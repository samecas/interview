FROM python:3

ENV GITHUB_TOKEN=ghp_xxxxxx
ENV MAIL_USER=sender
ENV MAIL_PASS=Test21123
ENV MAIL_HOST=mail.example.com
ENV MAIL_FROM=sender@example.com
ENV MAIL_TO=recipient@example.com

ADD main.py /

RUN pip install requests

CMD [ "python", "-u", "./main.py" ]
