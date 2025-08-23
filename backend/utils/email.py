import sendgrid
from sendgrid.helpers.mail import Mail
from config import settings
from utils.logging import logger

def send_email(to_email, subject, content):
    if not settings.SENDGRID_API_KEY:
        logger.warning("SendGrid API key not configured")
        return False
    
    message = Mail(
        from_email="noreply@nextgenrealty.com",
        to_emails=to_email,
        subject=subject,
        html_content=content)
    
    try:
        sg = sendgrid.SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        logger.error(f"Email send failed: {str(e)}")
        return False