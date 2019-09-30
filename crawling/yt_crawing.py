from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd
from selenium import webdriver 
import os
import requests
import ssl
import json
import time
import csv

# For ignoring SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#setting path
channelPath = r'your\path\\channel_url_req_1.txt'
csv_name = 'yt_summary_1.csv'


connect_url = 'https://www.youtube.com'
cross_limit = '&has_verified=1'  #通過限制級

save_con_url_count = []

title_count = []
channel_name_count = []
time_count = []
categorical_count = []
view_count = []
like_count = []
dislike_count = []
subscribe_count = []
hashtag_count = []

YT_df = {}

def Soup(url):
    got_url = requests.get(url)
    data = got_url.text
    soup = bs(data,'html.parser')

    return soup
    
def Load_int(string):
    #從字串挑出數字
    return int(''.join(x for x in string if x.isdigit()))

def Get_element(soup,connect_vid):
    temp_hashtags = []
    #片名
    if (soup.findAll('span',attrs={'class': 'watch-title'}) == []):
        title_count.append(np.nan)
    else:
        for span in soup.findAll('span',attrs={'class': 'watch-title'}):
            title_count.append(span.text.strip())
            print(span.text.strip())
            
    #youtuber name
    if (soup.findAll('script',attrs={'type': 'application/ld+json'}) == []):
        channel_name_count.append(np.nan)
    else:
        for script in soup.findAll('script',attrs={'type': 'application/ld+json'}):
            channelDesctiption = json.loads(script.text.strip())
            channel_name_count.append(channelDesctiption['itemListElement'][0]['item']['name'])
            print(channelDesctiption['itemListElement'][0]['item']['name'])
    
    #觀看時間
#    for strong in soup.findAll('strong',attrs={'class':"watch-time-text"}):    
#        try:
#            time_count.append(Load_int(strong.text.strip()))
#            print(Load_int(strong.text.strip()))
#        except:
#            time_count.append(np.nan)
    
    #影片分類(容易有問題加上try)
    try:    
        for a in soup.findAll('a',attrs={'class':"yt-uix-sessionlink spf-link"})[-1]:
            categorical_count.append(a)
            print(a)
    except:
        categorical_count.append(np.nan)
        print('a except')
        
    #觀看次數
    for div in soup.findAll('div',attrs={'class': 'watch-view-count'}):
        try:
            view_count.append(Load_int(div.text.strip()))
        except:
            view_count.append(np.nan)
    
    #喜歡次數
    for button in soup.findAll('button',attrs={'title': '我喜歡'}):  #中文網站 title:我喜歡 英文網站:I like it
        try:
            like_count.append(Load_int(button.text.strip()))
        except:
            like_count.append(np.nan)
    
    #不喜歡次數
    for button in soup.findAll('button',attrs={'title': '我不喜歡'}): #中文網站 title:我不喜歡 英文網站:I dislike it
        try:
            dislike_count.append(Load_int(button.text.strip()))
            break
        except:
            dislike_count.append(np.nan)

    #problem with 18x limitation so it can't catch subscriber
    if (soup.findAll('span',attrs={'class': 'yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count'}) == []):
        if channel_name_count[-1] == channel_name_count[-2]:  
            #視為同個頻道
            subscribe_count.append(subscribe_count[-2])
        else:
            subscribe_count.append(np.nan)
    else:
        for span in soup.findAll('span',attrs={'class': 'yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count'}):
            try:
                subscribe_count.append(Load_int(span.text.strip()))
            except:
                subscribe_count.append(np.nan)
    if (soup.findAll('span',attrs={'class': 'standalone-collection-badge-renderer-text'}) == []):
        temp_hashtags.append(np.nan)
    else:
        for span in soup.findAll('span',attrs={'class': 'standalone-collection-badge-renderer-text'}):
            for a in span.findAll('a',attrs={'class': 'yt-uix-sessionlink'}):
                temp_hashtags.append(a.text.strip().lstrip('#'))
    hashtag_count.append(temp_hashtags)
    
    Tran_dataframe()

def Tran_dataframe():
    
    with open(csv_name, 'a+',newline='',encoding="utf-8") as csvfile:
        #filenames = ['Title','Channel','Views','Like','Dislike','Subscriber','Hashtag','categorical']
        writer = csv.writer(csvfile)
        #writer = csv.DictWriter(csvfile,fieldnames=filenames)
        #時間
        writer.writerow([title_count[-1],channel_name_count[-1],view_count[-1],
                          like_count[-1],dislike_count[-1],subscribe_count[-1],
                          hashtag_count[-1],categorical_count[-1]])        
        
#        writer.writerow({'Title':title_count[-1],'Channel':channel_name_count[-1],'Views':view_count[-1],
#                          'Like':like_count[-1],'Dislike':dislike_count[-1],'Subscriber':subscribe_count[-1],
#                          'Hashtag':hashtag_count[-1],'categorical':categorical_count[-1]})
            
def main():    
    with open(csv_name, 'a+',newline='',encoding="utf-8") as csvfile:
        filenames = ['Title','Channel','Views','Like','Dislike','Subscriber','Hashtag','categorical']
        writer = csv.writer(csvfile)
        writer = csv.DictWriter(csvfile,fieldnames=filenames)
        
        writer.writeheader()
        
    
    file_url = list(open(channelPath,'r'))
    print(file_url)
    driver = webdriver.Chrome(executable_path=r'C:\Users\a4793\OneDrive\桌面\python\google driver\\chromedriver')
    for url in file_url:  
        
        driver.get(url)
        for _ in range(1,20):
            
            driver.execute_script('window.scrollTo(window.scrollTo(0, 10000000));')
            time.sleep(1)
        soup_links = bs(driver.page_source)
        links = soup_links.select('h3 a')

        for link in links:
            connect_vid = connect_url + link['href']
            soup_con = Soup(connect_vid)
            
            Get_element(soup_con,connect_vid)
            time.sleep(0.5)
    print(len(title_count))       
    print(len(channel_name_count)) 
    print(len(hashtag_count))
    #print(len(time_count))
    print(len(categorical_count))
    print(len(view_count))
    print(len(like_count))
    print(len(dislike_count))
    print(len(subscribe_count))
    
    
if __name__ == '__main__':
    main()