import globals

def email(sender, message):
    import smtplib, sys
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    password = globals.password
    subject = globals.subject
    smtpObj.login(sender, password)
    smtpObj.sendmail('SENDER-EMAIL', 'RECIPIENT-EMAIL', ("Subject: {}.\n{}").format(subject, message))
    smtpObj.quit
