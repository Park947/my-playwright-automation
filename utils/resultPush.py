"""
通知/推送模块：支持钉钉、邮件等通知方式
"""
import json
import hmac
import hashlib
import base64
import urllib.parse
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List, Optional
import requests
from utils.helper_methods import get_logger
from config.environments import env_manager


logger = get_logger()


class DingTalkNotifier:
    """钉钉通知类"""
    
    def __init__(self):
        """初始化钉钉通知器"""
        self.config = env_manager.get_dingtalk_config()
        self.enabled = self.config.get("enabled", False)
        self.webhook = self.config.get("webhook", "")
        self.secret = self.config.get("secret", "")
        self.keyword = self.config.get("keyword", "")
        self.at_all = self.config.get("at_all", False)
        self.at_mobiles = self.config.get("at_mobiles", [])
    
    def _sign(self, timestamp: str) -> str:
        """
        生成签名（如果配置了 secret）
        
        Args:
            timestamp: 时间戳（字符串）
        
        Returns:
            str: 签名
        """
        if not self.secret:
            return ""
        
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{self.secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign
    
    def send(self, title: str, content: str, at_all: bool = None, at_mobiles: List[str] = None):
        """
        发送钉钉消息
        
        Args:
            title: 消息标题
            content: 消息内容
            at_all: 是否@所有人（覆盖配置）
            at_mobiles: 需要@的手机号列表（覆盖配置）
        """
        if not self.enabled or not self.webhook:
            logger.warning("钉钉通知未启用或未配置 webhook")
            return
        
        # 构建消息
        message = {
            "msgtype": "markdown",
            "markdown": {
                "title": f"{self.keyword} - {title}",
                "text": f"## {self.keyword} - {title}\n\n{content}"
            }
        }
        
        # 添加@功能
        at_all = at_all if at_all is not None else self.at_all
        at_mobiles = at_mobiles if at_mobiles is not None else self.at_mobiles
        
        if at_all or at_mobiles:
            message["at"] = {
                "atMobiles": at_mobiles,
                "isAtAll": at_all
            }
        
        # 如果有签名，添加到 URL
        url = self.webhook
        if self.secret:
            timestamp = str(round(time.time() * 1000))
            sign = self._sign(timestamp)
            url = f"{self.webhook}&timestamp={timestamp}&sign={sign}"
        
        try:
            response = requests.post(url, json=message, timeout=10)
            response.raise_for_status()
            logger.info(f"钉钉通知发送成功: {title}")
        except Exception as e:
            logger.error(f"钉钉通知发送失败: {e}")
    
    def send_test_result(self, total: int, passed: int, failed: int, skipped: int, 
                        duration: str, report_url: str = ""):
        """
        发送测试结果通知
        
        Args:
            total: 总用例数
            passed: 通过数
            failed: 失败数
            skipped: 跳过数
            duration: 执行时长
            report_url: 报告链接（可选）
        """
        success_rate = (passed / total * 100) if total > 0 else 0
        
        content = f"""
### 测试执行完成

- **总用例数**: {total}
- **通过**: {passed} ✅
- **失败**: {failed} ❌
- **跳过**: {skipped} ⏭️
- **通过率**: {success_rate:.2f}%
- **执行时长**: {duration}

"""
        if report_url:
            content += f"- **报告链接**: [查看详情]({report_url})"
        
        self.send("测试执行报告", content)


class EmailNotifier:
    """邮件通知类"""
    
    def __init__(self):
        """初始化邮件通知器"""
        self.config = env_manager.get_email_config()
        self.enabled = self.config.get("enabled", False)
        self.smtp_server = self.config.get("smtp_server", "")
        self.smtp_port = self.config.get("smtp_port", 587)
        self.smtp_user = self.config.get("smtp_user", "")
        self.smtp_password = self.config.get("smtp_password", "")
        self.from_addr = self.config.get("from_addr", "")
        self.to_addrs = self.config.get("to_addrs", [])
        self.subject_prefix = self.config.get("subject_prefix", "[自动化测试]")
    
    def send(self, subject: str, content: str, to_addrs: List[str] = None):
        """
        发送邮件
        
        Args:
            subject: 邮件主题
            content: 邮件内容
            to_addrs: 收件人列表（覆盖配置）
        """
        if not self.enabled:
            logger.warning("邮件通知未启用")
            return
        
        if not self.smtp_server or not self.from_addr:
            logger.warning("邮件配置不完整")
            return
        
        to_addrs = to_addrs if to_addrs is not None else self.to_addrs
        if not to_addrs:
            logger.warning("未配置收件人")
            return
        
        try:
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = self.from_addr
            msg['To'] = ', '.join(to_addrs)
            msg['Subject'] = f"{self.subject_prefix} {subject}"
            
            # 添加正文
            msg.attach(MIMEText(content, 'html', 'utf-8'))
            
            # 发送邮件
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"邮件发送成功: {subject}")
        except Exception as e:
            logger.error(f"邮件发送失败: {e}")
    
    def send_test_result(self, total: int, passed: int, failed: int, skipped: int, 
                        duration: str, report_url: str = ""):
        """
        发送测试结果邮件
        
        Args:
            total: 总用例数
            passed: 通过数
            failed: 失败数
            skipped: 跳过数
            duration: 执行时长
            report_url: 报告链接（可选）
        """
        success_rate = (passed / total * 100) if total > 0 else 0
        
        content = f"""
        <html>
        <body>
            <h2>测试执行完成</h2>
            <table border="1" cellpadding="5">
                <tr><th>指标</th><th>数值</th></tr>
                <tr><td>总用例数</td><td>{total}</td></tr>
                <tr><td>通过</td><td style="color:green">{passed} ✅</td></tr>
                <tr><td>失败</td><td style="color:red">{failed} ❌</td></tr>
                <tr><td>跳过</td><td>{skipped} ⏭️</td></tr>
                <tr><td>通过率</td><td>{success_rate:.2f}%</td></tr>
                <tr><td>执行时长</td><td>{duration}</td></tr>
            </table>
        """
        if report_url:
            content += f'<p><a href="{report_url}">查看详细报告</a></p>'
        
        content += """
        </body>
        </html>
        """
        
        self.send("测试执行报告", content)


# 全局通知器实例
dingtalk_notifier = DingTalkNotifier()
email_notifier = EmailNotifier()


def send_test_notification(total: int, passed: int, failed: int, skipped: int, 
                          duration: str, report_url: str = ""):
    """
    发送测试通知（同时支持钉钉和邮件）
    
    Args:
        total: 总用例数
        passed: 通过数
        failed: 失败数
        skipped: 跳过数
        duration: 执行时长
        report_url: 报告链接（可选）
    """
    dingtalk_notifier.send_test_result(total, passed, failed, skipped, duration, report_url)
    email_notifier.send_test_result(total, passed, failed, skipped, duration, report_url)
