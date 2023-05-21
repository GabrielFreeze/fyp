import os
import sys
import signal
import requests
import pandas as pd
from methods import WebScraper
from selenium import webdriver
from selenium.webdriver.common.by import By

m = WebScraper(folder_name='malta_daily')

def signal_handler(sig,frame):
    pd.DataFrame(columns=['Title','Image Name','Body'],
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

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(m.CHROME_DRIVER_PATH, chrome_options=options)

data = []
count = 0

for pg_num in range(5,55):

    #Load next page
    driver.get(f'https://maltadaily.mt/category/news/local/page/{pg_num+1}/')

    #Get list of article links
    links = [i.find_element(By.TAG_NAME,'a').get_attribute('href') for i in 
             driver.find_elements(By.CLASS_NAME,'post-content-wrap')]
    
    for a in links:
        try:
            #Go to article
            driver.get(a)

            #Get title
            title = driver.find_elements(By.CLASS_NAME,'entry-title')[0].text
            
            #Get Body
            body = driver.find_elements(By.CLASS_NAME,'content-inner')[0].text.replace('\n','')
            
            #Get Image
            img_src  = driver.find_elements(By.CLASS_NAME,'wp-post-image')[0].get_attribute('src')
            img_name = f'img{str(count).zfill(5)}{get_img_ext(img_src)}' #Get image name
            img_data = requests.get(img_src).content #Download image
            count += 1

            #Write image
            with open(os.path.join(m.NEWS_IMG_PATH,img_name),'wb') as f:
                f.write(img_data)
            
            data.append([title,img_name,body])
        except: pass

#Save data to csv
pd.DataFrame(columns=['Title','Image Name','Body'],
             data=data).to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)
driver.quit()

