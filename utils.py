'''
MIT License

Copyright (c) 2017-2018 William Ivanski
Copyright (c) 2018 Israel Barth Rubio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import settings

if settings.SLACK['enabled']:
    from slackclient import SlackClient

def syscall(command):
    p = subprocess.run(command, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
    return {
        'stdout': p.stdout.decode('utf-8').split('\n')[:-1],
        'code': p.returncode
    }

def syscall_bg(command):
    subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    return None

def notify(p_text):
    if settings.SLACK['enabled']:
        sc = SlackClient(settings.SLACK['token'])
        sc.api_call(
          'chat.postMessage',
          channel=settings.SLACK['channel'],
          text=p_text,
          as_user='false',
          icon_url=settings.SLACK['bot_imageurl'],
          username=settings.SLACK['bot_name']
        )

def sendmail(p_from, p_to, p_subject, p_body, p_is_html):
    msg = MIMEMultipart()
    msg['From'] = p_from
    msg['To'] = ','.join(p_to)
    msg['Subject'] = p_subject
    if (p_is_html):
        msg.attach(MIMEText(p_body, 'html', 'utf-8'))
    else:
        msg.attach(MIMEText(p_body, 'plain', 'utf-8'))
    try:
        server = smtplib.SMTP(settings.MAIL['host'], settings.MAIL['port'])
        server.starttls()
        server.login(settings.MAIL['user'], settings.MAIL['password'])
        server.sendmail(p_from, p_to, msg.as_string())
    except Exception as exc:
        print(str(exc))
    finally:
        server.quit()
