# -*- coding: utf-8 -*-
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

from email import charset
charset.add_charset('utf-8', charset.SHORTEST, charset.BASE64, 'utf-8')

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to],charset='utf-8')##加入 charset 该关键字参数，使发送的html支持utf-8编码
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
