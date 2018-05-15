from bs4 import BeautifulSoup
import requests
import time
import os
import smtplib
from email.mime.text import MIMEText
import datetime
from pytz import timezone

def crawl():
    req =requests.get("http://m.ruliweb.com/news/board/1020")
    html = req.text
    soup = BeautifulSoup(html,'html.parser')
    titles = soup.select('tr > td > div.title.row > a.subject_link.deco')
    if os.path.isfile("temp.txt"):
        fp_r= open("temp.txt","r",encoding="utf8")
        saved_titles=list()
        for i in fp_r:
            saved_titles.append(i.rstrip())
        for i,title in enumerate(titles) :
            if any( a in title.text for a in ["pro","Pro","PRO","프로"]):
                if not title.text in saved_titles and title.text:

                    print("send email")
                    sendmail(titles[i])
    update_list(titles)
    print("crawled "+datetime.datetime.now(timezone('Asia/Seoul')).strftime("%H:%M:%S"))

def update_list(titles):
    fp = open("temp.txt", "w", encoding="utf8")
    for title in titles[4:]:
        print(title.text, file=fp)
    fp.close()
def sendmail(text):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()  # say Hello
    smtp.starttls()  # TLS 사용시 필요
    password = open("password.txt","r").readline()
    smtp.login('kdw9502@gmail.com', password)
    msg = MIMEText(text,"html",_charset="utf-8")
    msg['Subject'] = '플포 프로 정보 ! '+datetime.datetime.now(timezone('Asia/Seoul')).strftime("%H:%M:%S")
    msg['To'] = 'kdw9502@gmail.com'
    smtp.sendmail('kdw9502@gmail.com', 'kdw9502@gmail.com', msg.as_string())

    smtp.quit()
while(True):
    crawl()
    time.sleep(30)

