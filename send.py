import smtplib
import sys, os
from email.header import Header
from email.mime.text import MIMEText
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


class Send():
    def __init__(self, rece=None, title=None, uid=None, mail_host="發信站地址", mail_user="發信郵箱地址例如123@gmail.com",
                 mail_pass="發送密碼", sender="跟mail_user寫一樣就好"):
        self.rece = rece
        self.title = title
        self.uid = uid
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.sender = sender

    def readhtml(self, html="resource/mb.html"):
        with open(html, "rt", encoding='utf-8') as f:
            self.mb = f.read()

    def setUid(self, uid):
        self.uid = uid

    def setRece(self, recev):
        self.rece = recev

    def setTitle(self, title):
        self.title = title

    def formatHtml(self):
        if self.uid == None:
            self.content = self.mb
        else:
            self.content = self.mb.format(self.uid)

    def sendEmail(self):
        self.formatHtml()
        message = MIMEText(self.content, 'html', 'utf-8')
        message['From'] = "{}".format(self.sender)
        message['To'] = self.rece
        message['Subject'] = self.title

        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, self.rece, message.as_string())
            print("[INFO] mail has been send successfully.")
            return 1
        except smtplib.SMTPException as e:
            print(e)
            return 0
