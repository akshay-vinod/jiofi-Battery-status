import requests
import time
from bs4 import BeautifulSoup
import smtplib
import time
from pygame import mixer


def playlowbattery():
    mixer.init()
    mixer.music.load('battery_low_alert.mp3')
    mixer.music.play()
    print("CONNECT YOUR CHARGER!!")


def playbatteryfull():
    mixer.init()
    mixer.music.load('battery_is_at_100.mp3')
    mixer.music.play()
    print("DISCONNECT YOUR CHARGER!!")


def playcharging():
    mixer.init()
    mixer.music.load('battery_is_charging.mp3')
    mixer.music.play()


def playdischarging():
    mixer.init()
    mixer.music.load('disconnected.mp3')
    mixer.music.play()


def check_battery():
    batterystate = 0
    url = "http://jiofi.local.html/"

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}

    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')  # load site content
    """ print(soup) """

    # fetch battery percentage
    batterylvl = soup.select_one('#batterylevel')['value']
    # fetch battery connected to battery or not
    battery_connection_status = soup.select_one('#batterystatus')['value']
    print(batterylvl + " " + time.strftime("%H:%M:%S"))
    percentageNum = int(''.join(filter(lambda i: i.isdigit(), batterylvl)))
    if(percentageNum < 10):
        playlowbattery()
    elif(percentageNum == 100):
        batterystate = 1
    if(percentageNum != 100):
        batterystate = 2
    connection_status(battery_connection_status)
    return batterystate


charging_flag = 0
discharging_flag = 0


def connection_status(status):
    global discharging_flag, charging_flag
    if(status == "Discharging"):
        charging_flag = 0
        if(discharging_flag == 0):
            playdischarging()
            print("Discharging")
            discharging_flag = discharging_flag+1
    elif(status == "Charging"):
        discharging_flag = 0
        if(charging_flag == 0):
            playcharging()
            print("charging")
            charging_flag = charging_flag+1


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
n = 0
while(True):
    batteryState = check_battery()
    if(batteryState == 2):
        n = 0
    elif(batteryState == 1):
        if(n == 0):
            playbatteryfull()
            n = n+1
    time.sleep(1)  # check price in every 1 min
