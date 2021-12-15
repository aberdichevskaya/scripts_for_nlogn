# -*- coding: utf-8 -*- 

import os
import re
import csv
import mimetypes
from optparse import OptionParser
import smtplib
from email.message import EmailMessage


email_re = r"\A[a-zA-Z0-9!#$%&'*+/=?^_‘{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_‘{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\Z"

def send(srv, opts, msg):
    em = EmailMessage()
    em.set_content(msg)
    em["Subject"] = opts.subject
    em["From"] = f"{opts.from_name} <{opts.from_addr}>"
    em["To"] = opts.to_addr
    if not re.fullmatch(email_re, opts.to_addr):
        print(f"Wrong email: {opts.to_addr}")
    else:
        try:
            srv.send_message(em)
        except Exception as e:
            # print(e)
            print(f"Error: {opts.to_addr}")
        else:
            print(f"Sent: {opts.to_addr}")

def spam(srv, opts, msg):
    with open(opts.data, encoding="utf-8") as csv_file:
        dr = csv.DictReader(csv_file, delimiter=';')
        for entry in dr:
            opts.to_addr = entry["email"]
            send(srv, opts, msg.format(**entry))

def main():
    op = OptionParser()

    msg, val = "SMTP host", "smtp.misis.ru"
    op.add_option("-s", "--server", dest="host", default=val, help=msg)

    msg, val = "SMTP port", 587
    op.add_option("-P", "--port", dest="port", default=val, help=msg)

    msg, val = "SMTP user", "programming-acm1"
    op.add_option("-u", "--user", dest="user", default=val, help=msg)

    msg, val = "SMTP password", "KloJhep1"
    op.add_option("-p", "--password", dest="password", default=val, help=msg)

    msg, val = "sender email", "programming-acm@misis.ru"
    op.add_option("-f", "--from", dest="from_addr", default=val, help=msg)

    msg, val = "sender name", "Олимпиада \"Когнитивные Технологии\""
    #msg, val = "sender name", "ACM MISIS"
    op.add_option("-x", "--sender", dest="from_name", default=val, help=msg)

    msg, val = "receiver email", ""
    op.add_option("-t", "--to", dest="to_addr", default=val, help=msg)

    #msg, val = "email subject", u"Ваша регистрация не завершена"
    msg, val = "email subject", u"Повторная рассылка данных для входа в тестирующую систему"
    op.add_option("-y", "--subject", dest="subject", default=val, help=msg)

    msg, val = "data CSV: \"email,...\"", ""
    op.add_option("-d", "--data", dest="data", default=val, help=msg)

    (opts, args) = op.parse_args()
    
    if not (opts.subject and opts.password and (opts.to_addr or opts.data)):
        op.print_help()
    elif opts.data and opts.to_addr:
        print("You need specify only one option (--to or --data)")
    else:
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            lines.append(line)
        msg = '\n'.join(lines)
        try:
            srv = smtplib.SMTP(opts.host, opts.port)
            srv.ehlo()
            srv.starttls()
            srv.login(opts.user, opts.password)
        except:
            print("SMTP server connection error!")
        else:
            try:
                if opts.to_addr:
                    send(srv, opts, msg)
                else:
                    spam(srv, opts, msg)
            except Exception as e:
                print(e)
                print("Email sending error!")
            else:
                print("All emails successfully sent.")
            finally:
                srv.quit()

if __name__ == "__main__":
    main()