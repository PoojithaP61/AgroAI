import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.config import settings

# Configure logger
logger = logging.getLogger(__name__)

class NotificationService:
    """
    Service for sending notifications (Email, SMS).
    """
    
    @staticmethod
    def send_email(to_email: str, subject: str, content: str):
        """
        Send an email using SMTP (e.g., Gmail).
        Falls back to logging if credentials are not provided.
        """
        if not settings.EMAIL_SENDER or not settings.EMAIL_PASSWORD:
            logger.warning("EMAIL_SENDER or EMAIL_PASSWORD not set. Logging email instead.")
            return NotificationService._log_mock_email(to_email, subject, content)

        try:
            msg = MIMEMultipart()
            msg['From'] = settings.EMAIL_SENDER
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(content, 'plain'))

            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    @staticmethod
    def _log_mock_email(to_email: str, subject: str, content: str):
        """Helper to log email when real sending is disabled"""
        logger.info(f"========== MOCK EMAIL SEND ==========")
        logger.info(f"To: {to_email}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Content: {content}")
        logger.info(f"=====================================")
        print(f"\n[EMAIL] To: {to_email} | Subject: {subject} | Content: {content}\n")
        return True

    @staticmethod
    def send_sms(to_phone: str, content: str):
        """
        Simulate sending an SMS.
        """
        logger.info(f"=========== MOCK SMS SEND ===========")
        logger.info(f"To: {to_phone}")
        logger.info(f"Content: {content}")
        logger.info(f"=====================================")
        print(f"\n[SMS] To: {to_phone} | Content: {content}\n")
        return True

    @staticmethod
    def send_verification_code(contact_info: str, code: str, via: str = "EMAIL"):
        """
        Send a verification code via Email or SMS
        """
        if via == "EMAIL":
            subject = "AgroAI Verification Code"
            content = f"Your verification code is: {code}. It expires in 10 minutes."
            return NotificationService.send_email(contact_info, subject, content)
        elif via == "SMS":
            content = f"Your AgroAI code is: {code}"
            return NotificationService.send_sms(contact_info, content)
        return False
