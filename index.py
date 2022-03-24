from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import datetime
import time
import pywhatkit
import schedule
import os

def writeFile(name, title):
    try:
        f = open(name+".txt", "a+")
        f.write(title.strip())
        f.write('\n')
        f.close()
    except:
        print(title)

def readFile(name):
    file = name+".txt"
    list = []
    if os.path.exists(file):
        with open(file, 'r') as f:
            list = [line.strip() for line in f]
    return list

def job():

    scanned = 'scanned-channels'
    unscanned = 'channels'
    
    service = Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)

    channels_list = readFile(unscanned)
    scanned_list = readFile(scanned)
    final_channel_url = channels_list[-1]
    if len(channels_list) == len(scanned_list) and os.path.exists(scanned+".txt"):
        os.remove(scanned+".txt")

    for channelUrl in channels_list:
        if channelUrl not in scanned_list:
            writeFile(scanned, channelUrl)
            driver.get(channelUrl)
            
            channel_name = driver.find_element(By.CLASS_NAME, "ytd-channel-name").text
            try:
                video_title_list = driver.find_elements(By.ID,"video-title")
                meta_div = driver.find_element(By.ID, "metadata-line")
                meta_data = meta_div.find_elements(By.TAG_NAME, "span")

                if(len(meta_data) == 2):
                    views = meta_data[0].text
                    posted = meta_data[1].text
                if(len(meta_data) == 1):
                    posted = meta_data[0].text
                    views = "Unavailable"
                    

                latest = video_title_list[0].text
                href = video_title_list[0].get_attribute("href")
                
                info_string = "Channel: "+channel_name+", Title: " + latest + ", Views: " + views + ", Posted: " + posted +", Url: "+ href

                try:
                    skip_list = readFile(channel_name)

                    if(latest not in skip_list):                
                        writeFile(channel_name, latest)

                        now  = datetime.datetime.now()
                        try:
                            if "days" not in posted and "week" not in posted and "month" not in posted and "year" not in posted:
                                pywhatkit.sendwhatmsg("+254710139182",info_string, now.hour, now.minute+1)
                        except:
                            print("Unable to send message")
                except:
                    print(channel_name + " not available")
            except:
                print("no vids")
        if (channelUrl == final_channel_url):
            driver.close()
        

# Run script hourly
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)