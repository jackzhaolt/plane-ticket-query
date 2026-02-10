"""Email notification system for flight deals."""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List


class EmailNotifier:
    """Send email alerts for flight deals."""

    def __init__(self):
        """Initialize email notifier with SMTP configuration."""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.username = os.getenv('SMTP_USERNAME')
        self.password = os.getenv('SMTP_PASSWORD')
        self.recipient = os.getenv('ALERT_EMAIL')

        if not all([self.username, self.password, self.recipient]):
            raise ValueError(
                "Email configuration incomplete. "
                "Set SMTP_USERNAME, SMTP_PASSWORD, and ALERT_EMAIL in .env file."
            )

    def send_alert(self, subject: str, body: str, deals_count: int = 1):
        """
        Send an email alert.

        Args:
            subject: Email subject line
            body: Email body content
            deals_count: Number of deals in this alert
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"✈️ {subject}"
            msg['From'] = self.username
            msg['To'] = self.recipient

            # Create HTML version
            html_body = self._create_html_body(body, deals_count)

            # Attach both plain text and HTML
            msg.attach(MIMEText(body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            print(f"✓ Email alert sent to {self.recipient}")

        except Exception as e:
            print(f"✗ Failed to send email: {e}")

    def send_deals_alert(self, deals_summary: List[str]):
        """
        Send an alert with multiple flight deals.

        Args:
            deals_summary: List of formatted deal strings
        """
        count = len(deals_summary)
        subject = f"{count} Flight Deal{'s' if count > 1 else ''} Found!"

        body = f"Found {count} great flight deal{'s' if count > 1 else ''}:\n\n"
        body += "\n\n" + "="*60 + "\n\n".join(deals_summary)
        body += "\n\nHappy travels! ✈️"

        self.send_alert(subject, body, count)

    def _create_html_body(self, plain_text: str, deals_count: int) -> str:
        """
        Create an HTML version of the email body.

        Args:
            plain_text: Plain text version
            deals_count: Number of deals

        Returns:
            HTML formatted email body
        """
        html = f"""
        <html>
          <head>
            <style>
              body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
              .header {{ background-color: #0066cc; color: white; padding: 20px; text-align: center; }}
              .content {{ padding: 20px; }}
              .deal {{ background-color: #f5f5f5; padding: 15px; margin: 15px 0; border-left: 4px solid #0066cc; }}
              .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            </style>
          </head>
          <body>
            <div class="header">
              <h1>✈️ Flight Deal Alert</h1>
              <p>{deals_count} great deal{'s' if deals_count > 1 else ''} found!</p>
            </div>
            <div class="content">
              <pre>{plain_text}</pre>
            </div>
            <div class="footer">
              <p>Sent by Plane Ticket Query System</p>
            </div>
          </body>
        </html>
        """
        return html
