import requests
import os
from datetime import datetime, timedelta
import time
import smtplib, ssl
from email.mime.text import MIMEText

token = os.getenv('GITHUB_TOKEN', '...')
mail_username = os.getenv('MAIL_USER', '...')
mail_password = os.getenv('MAIL_PASS', '...')
mail_host = os.getenv('MAIL_HOST', '...')

def sendsmtp(commitnum,mailbody):
  sender_email = os.getenv('MAIL_FROM', '...')
  receiver_email = os.getenv('MAIL_TO', '...')
  msg = MIMEText(mailbody)
  msg['Subject'] = "found new commits: " + commitnum

  port = 465
  context = ssl.create_default_context()
  context.set_ciphers('DEFAULT')

  with smtplib.SMTP_SSL("mail.policija.lt", port, context=context) as server:
    server.login(mail_username, mail_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())

lastnow = datetime.now()
lastrun = lastnow.strftime("%Y-%m-%dT%H:%M")
mailsent = 0

while True:
  now = datetime.now()
  till_now = now.strftime("%Y-%m-%dT%H:%M")
  after_1days = lastnow + timedelta(days = 1)
  print("running API query from:", lastrun, "till", till_now)
  query_url = f"https://api.github.com/search/commits?q=committer-email:torvalds@linux-foundation.org+committer-date:{lastrun}..{till_now}"
  params = {
    "state": "open",
    }
  headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f'token {token}'
  }
  r = None
  while r is None:
    try:
       r = requests.get(query_url, headers=headers, params=params)
    except requests.exceptions.RequestException as e:
       print(f"[!] Exception caught - Retrying...: {e}")
       time.sleep(30)
  jsonResponse = r.json()
  foundcommits = jsonResponse["total_count"]
  commits = []
  for i in jsonResponse["items"]:
    commit_new = i["html_url"]
    commits.append(commit_new)
  if foundcommits > 0:
    if mailsent == 0:
      print("sending email. Total new commits found:",foundcommits)
      sendsmtp(str(foundcommits),str(commits))
      mailsent = 1
      lastrun = now.strftime("%Y-%m-%dT%H:%M")
      lastnow = datetime.now()
    else:
      if now > after_1days:
        print("sending email. Total new commits found:",foundcommits)
        sendsmtp(str(foundcommits),str(commits))
        mailsent = 1
        lastrun = now.strftime("%Y-%m-%dT%H:%M")
        lastnow = datetime.now()
      else:
        print("email was sent already today. Total new commits found:",foundcommits)
  else:
    print("No new commits found - sleeping...")

  time.sleep(600)
