import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from core.logger import logger


class EmailSender:
    def __init__(self, mail_sender, mailhog_host, mailhog_port):
        self.mail_sender = mail_sender
        self.mailhog_host = mailhog_host
        self.mailhog_port = mailhog_port

    def _send_email(self, recipient, subject, body):
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.mail_sender
            msg['To'] = recipient

            server = smtplib.SMTP(self.mailhog_host, self.mailhog_port)
            server.sendmail(self.mail_sender, recipient, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            logger.info(f"Failed to send email: {e}")
            return False

    def _send_email_with_attachment(self, recipient, subject, body, report_path=None):
        try:
            msg = MIMEMultipart()
            msg['Subject'] = 'Weekly Report'
            msg['From'] = self.mail_sender
            msg['To'] = recipient

            # Attach the text message
            msg.attach(MIMEText(body, 'plain'))

            # Attach a JSON file
            json_file = 'weekly_report.json'
            with open(report_path, 'rb') as f:
                attachment = MIMEApplication(f.read(), Name=report_path)
                attachment['Content-Disposition'] = f'attachment; filename="{json_file}"'
                msg.attach(attachment)

            # Send the email via MailHog
            server = smtplib.SMTP(self.mailhog_host, self.mailhog_port)
            server.sendmail(self.mail_sender, recipient, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            logger.info(f"Failed to send email: {e}")
            return False

    def send_overdue_email(self, patron_email, patron_name, book_title, days_overdue):
        body = f"""
        Dear {patron_name},

        This is a reminder that the book '{book_title}' 
        is {days_overdue} days overdue. 

        Please return the book to the library as soon as possible.

        Best regards,
        Library Management
        """
        subject = 'Overdue Book Reminder'
        return self._send_email(patron_email, subject, body)

    def send_weekly_statistics_email(self, report_path, recipient):
        body = f"""
        Dear {recipient},

        This is a weekly statistics report of books.
        """
        subject = 'Weekly statistics report'

        return self._send_email_with_attachment(recipient, subject, body, report_path)