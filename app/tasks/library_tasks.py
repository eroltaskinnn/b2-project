from email.mime.multipart import MIMEMultipart

from sqlalchemy import func

from crud.checkout_crud import CheckoutCRUD
from models.patron import Patron
from models.book import Book
from models.checkout import Checkout
from datetime import datetime, timedelta


from core.config import settings
from core.database import SessionLocal
from tasks.celery_config import celery_app
from core.logger import logger
from utils.email_sender import EmailSender
from utils.weekly_report_saver import WeeklyReportSaver


@celery_app.task
def send_overdue_reminders():
    logger.info(f"starting to send overdue reminders")

    """Send email reminders for overdue books"""
    db = SessionLocal()
    try:
        query = CheckoutCRUD(db)

        overdue_checkouts = query.get_overdue_books()
        logger.info(f"preparing for sending overdue reminders")

        email_sender = EmailSender(settings.MAIL_SENDER,
                                   settings.MAILHOG_HOST,
                                   settings.MAILHOG_PORT)

        # Send reminder emails
        for checkout in overdue_checkouts:
            email_sender.send_overdue_email(checkout.patron.email,
                                            checkout.patron.name,
                                            checkout.book.title,
                                            (datetime.utcnow() - checkout.due_date).days)


            logger.info(f"Overdue email sent to {checkout.patron.email} for book: {checkout.book.title}")

        return f"Sent {len(overdue_checkouts)} overdue reminders"
    except Exception as exc:
        logger.info(f"Failed to send overdue reminders: {exc}")
    finally:
        db.close()

@celery_app.task
def generate_weekly_report():
    """Generate weekly checkout statistics report"""
    db = SessionLocal()
    logger.info(f"starting to generate weekly report")

    try:
        query = CheckoutCRUD(db)
        # Calculate date range for the past week
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)

        total_checkouts = query.get_total_checkouts(start_date=start_date,
                                                    end_date=end_date)

        popular_books = query.get_popular_books(start_date=start_date,
                                                    end_date=end_date)

        # Generate report (could save to file or send via email)
        report = {
            'period_start': str(start_date),
            'period_end': str(end_date),
            'total_checkouts': total_checkouts,
            'popular_books': [
                {
                    'title': book.title,
                    'checkout_count': count
                } for book, count in popular_books
            ]
        }

        report_saver = WeeklyReportSaver()
        report_file = report_saver.save(report)

        email_sender = EmailSender(settings.MAIL_SENDER, settings.MAILHOG_HOST, settings.MAILHOG_PORT)
        email_sender.send_weekly_statistics_email(report_file, settings.SYSTEM_ADMIN)

        logger.info(f"Report saved to {report_file}")

        return report
    except Exception as exc:
        logger.info(f"Failed to generate weekly report: {exc}")
    finally:
        db.close()

