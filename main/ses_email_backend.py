import os
import boto3
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class SESBackend(BaseEmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = boto3.client(
            'ses',
            region_name='ap-southeast-2',
            aws_access_key_id=os.getenv('AWS_SES_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SES_SECRET_ACCESS_KEY')
        )

    def send_messages(self, email_messages):
        """Send a list of EmailMessage objects using SES"""
        sent_count = 0
        for message in email_messages:
            try:
                response = self.client.send_email(
                    Source=message.from_email,
                    Destination={'ToAddresses': message.to},
                    Message={
                        'Subject': {'Data': message.subject},
                        'Body': {'Text': {'Data': message.body}},
                    }
                )
                sent_count += 1
            except Exception as e:
                self.fail_silently = False
                print(f"Error sending email: {e}")
        return sent_count
