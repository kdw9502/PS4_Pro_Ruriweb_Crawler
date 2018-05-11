from bs4 import BeautifulSoup
import requests
import time
import os
import smtplib
from email.mime.text import MIMEText
import datetime
from pytz import timezone

def crawl():
    req =requests.get("http://m.ruliweb.com/news/board/1020/list?cate=1")
    html = req.text
    soup = BeautifulSoup(html,'html.parser')
    titles = soup.select('tr > td > div.title.row > a.subject_link.deco')

    if not os.path.isfile("temp.txt"):
        fp= open("temp.txt","w",encoding="utf8")
        for title in titles[4:]:
            print(title.text,file=fp)
        fp.close()
        return
    else:
        fp_r= open("temp.txt","r",encoding="utf8")
        saved_titles=list()
        for i in fp_r:
            saved_titles.append(i.rstrip())
        for i,title in enumerate(titles) :
            if any( a in title.text for a in ["pro","Pro","PRO","프로"]):
                if not title.text in saved_titles and title.text:
                    print(saved_titles)
                    print(title.text)
                    #sendmail(titles[i])
    print("crawled "+datetime.datetime.now(timezone('Asia/Seoul')).strftime("%H:%M:%S"))

def sendmail(text):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()  # say Hello
    smtp.starttls()  # TLS 사용시 필요
    password = open("password.txt","r").readline()
    smtp.login('kdw9502@gmail.com', password)
    msg = MIMEText(text)
    msg['Subject'] = '플포 프로 정보 ! '+datetime.datetime.now(timezone('Asia/Seoul')).strftime("%H:%M:%S")
    msg['To'] = 'kdw9502@gmail.com'
    smtp.sendmail('kdw9502@gmail.com', 'kdw9502@gmail.com', msg.as_string())

    smtp.quit()
while(True):
    crawl()
    time.sleep(60)
