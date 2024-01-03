import os
import sys
import signal
import requests
import pandas as pd
from time import sleep
from datetime import datetime
from selenium import webdriver
from ws_methods import WebScraper
from selenium.webdriver.common.by import By

m = WebScraper(folder_name='malta_daily')

def signal_handler(sig,frame):
    print('SIG Received - Saving..')
    pd.DataFrame(columns=columns,
            data=data).to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)
    driver.quit()
    sys.exit()
def get_img_ext(img_link):

    if img_link.endswith('.jpeg'):
        return '.jpeg'
    elif img_link.endswith('.jpg'):
        return '.jpg'
    elif img_link.endswith('.png'):
        return '.png'
    else: return ""

signal.signal(signal.SIGINT, signal_handler)

driver = webdriver.Chrome(m.CHROME_DRIVER_PATH)

data = []
columns = ['Title','Author','Date','Image Name','Caption','Body','URL']
img_count = 0

num_pgs = 100
save_every = 5
assert num_pgs%save_every == 0

for pg_idx in range(num_pgs+1):

    #Load next page
    driver.get(f'https://maltadaily.mt/category/news/local-news/page/{pg_idx+1}')

    #Get list of article links
    links = [a.get_attribute('href') for a in driver.find_elements(By.CLASS_NAME,'entire-meta-link')]
        
    for a in links:
        try:
            #Go to article
            driver.get(a)
            sleep(0.65)

            #Get Title
            title = driver.find_elements(By.CLASS_NAME,'entry-title')[0].text
            print(f'Extracting: {title[:30]}... ',end='')

            #Get Date
            date = driver.find_element(By.XPATH,'//*[@id="single-below-header"]/span[1]').text
            date = datetime.strptime(date,"%b %d %Y").strftime('%d-%m-%Y')

            #Get URL
            url = driver.current_url            
            
            #Get Body
            body = driver.find_elements(By.CLASS_NAME,'content-inner')[0].text.replace('\n','')
            
            #Get Image
            img_src  = driver.find_elements(By.CLASS_NAME,'wp-post-image')[0].get_attribute('src')
            img_name = f'img{str(img_count).zfill(5)}{get_img_ext(img_src)}' #Get image name
            img_data = requests.get(img_src).content #Download image
            img_count += 1

            #Write image
            with open(os.path.join(m.NEWS_IMG_PATH,img_name),'wb') as f:
                f.write(img_data)
            
            #Add row
            data.append([title,'',date,img_name,'',body,url])

            print('[OK]')
        except Exception as e:
            print(f'[ERR]')

    #Save to csv
    if pg_idx%save_every == 0:
        print('\nSaving...')
        (pd.DataFrame(columns=columns,data=data)
            .to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)) 
