import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def SendaEmail(toEmail, username):
    myemail='1130245684@qq.com'
    otheremail=toEmail
    password='yaqtjpbvjsivjcfb'
    msg  = MIMEMultipart()
    msg['to'] = otheremail
    msg['from'] = myemail
    msg['subject'] = "Pinocchio's Pizza & Subs.Thank you for your purchase."
    context = username + ", we have already received your ordered! We will cook the food for you as soon as possible. Please feel free to contact us if you have any questions. Email:1130245684@qq.com"
    part = MIMEText(context)
    msg.attach(part)
    server = smtplib.SMTP_SSL("smtp.qq.com",timeout=30)
    server.set_debuglevel(0)
    server.ehlo("smtp.qq.com")
    server.login(myemail,password)
    server.sendmail(msg['from'], msg['to'],msg.as_string())
    server.close()
