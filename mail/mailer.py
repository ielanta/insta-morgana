import smtplib
from email.mime.text import MIMEText
from settings import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, OBSERVER_EMAIL


class Mailer:
    def __init__(self):
        self.server = smtplib.SMTP_SSL(EMAIL_HOST)
        self.sender_email = EMAIL_HOST_USER
        self.server.login(self.sender_email, EMAIL_HOST_PASSWORD)

    @staticmethod
    def make_message(subject: str, text: str, from_email: str, to_email: str):
        msg = MIMEText(text, 'html')
        msg['Subject'] = subject
        msg['From'] = f'InstaInformer <{from_email}>'
        msg['To'] = to_email
        return msg

    def send_mail(self, subject: str, msg_text: str) -> None:
        msg = self.make_message(subject=subject, text=msg_text, from_email=self.sender_email, to_email=OBSERVER_EMAIL)
        self.server.sendmail(msg['From'], msg['To'], msg.as_string())

    def send_mail_new_media_found(self, user_id: str, new_media: list) -> None:
        subject = f'{user_id} published a post'.capitalize()
        text = f'<h4>Check it out: https://instagram.com/{user_id} </h4>'
        for media in new_media:
            text += f"<div><p>{media['description']}</p><img src='{media['link']}' width='640'></div><br/>"
        self.send_mail(subject, text)

    def send_mail_stories_found(self, user_id: str) -> None:
        subject = f'{user_id} published a story'.capitalize()
        text = f'<h4>Check it out: https://instagram.com/{user_id} </h4>'
        self.send_mail(subject, text)
