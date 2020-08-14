import requests
from bs4 import BeautifulSoup
import smtplib
import time
from pygame import mixer
def play():
    mixer.init()
    mixer.music.load('846_download_battery_low_ringtone.mp3')
    mixer.music.play()
    print("CONNECT YOUR CHARGER!!")
def check_battery():
    url = "http://jiofi.local.html/"

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
        
    page = requests.get(url, headers=headers)

    soup =  BeautifulSoup(page.content, 'html.parser') #load site content

    # fetch battery percentage
    battery = soup.select_one('#batterylevel')['value']
    print(battery)
    percentageNum = int(''.join(filter(lambda i: i.isdigit(), battery)))
    if(percentageNum < 10):
        play()


    
""" send email at low battery level
def send_mail():
        creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)

        start TLS for security
        s.starttls()

        Authentication
        s.login("sender_email_id", "sender_email_id_password") 

        message to be sent
        message = " "

        sending the mail
        s.sendmail("sender_email_id", "receiver_email_id", message)

        terminating the session
        s.quit()
        print("email has been send") """
while(True):
     check_battery()
     time.sleep(60) #check price in every 1 min


        
