"""SMS notification system for flight deals."""

import os
from typing import Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


class SMSNotifier:
    """Send SMS alerts for flight deals using Twilio."""

    def __init__(self):
        """Initialize Twilio client."""
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.to_number = os.getenv('ALERT_PHONE_NUMBER')

        if not all([self.account_sid, self.auth_token, self.from_number, self.to_number]):
            raise ValueError(
                "SMS configuration incomplete. "
                "Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, "
                "TWILIO_PHONE_NUMBER, and ALERT_PHONE_NUMBER in .env file."
            )

        self.client = Client(self.account_sid, self.auth_token)

    def send_alert(self, message: str):
        """
        Send an SMS alert.

        Args:
            message: SMS message content (max 1600 chars for long messages)
        """
        try:
            # Truncate message if too long
            if len(message) > 1600:
                message = message[:1597] + "..."

            # Send SMS
            response = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=self.to_number
            )

            print(f"✓ SMS alert sent to {self.to_number} (SID: {response.sid})")

        except TwilioRestException as e:
            print(f"✗ Failed to send SMS: {e}")

    def send_deals_alert(self, deals_count: int, top_deal_summary: str):
        """
        Send a concise SMS alert about deals found.

        Args:
            deals_count: Number of deals found
            top_deal_summary: Summary of the best deal
        """
        message = f"✈️ {deals_count} flight deal{'s' if deals_count > 1 else ''} found!\n\n"
        message += "Top deal:\n"
        message += top_deal_summary

        self.send_alert(message)
