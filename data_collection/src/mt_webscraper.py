import os
import sys
import signal
import requests
import pandas as pd
from time import time
from time import sleep
from methods import WebScraper
from selenium import webdriver
from selenium.webdriver.common.by import By

m = WebScraper(folder_name='malta_today')

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

#Load initial page
driver.get('https://www.maltatoday.com.mt/news/national/1/')

#Remove inital cookie pop-up
driver.find_element(By.XPATH,'/html/body/div[2]/div/div/button').click()

img_count = 0
data = []

#0,1,12-17 are not links we want to click
idx_lst = [2,3,4,5,6,7,8,9,10,11,18,19,20,21,22,23,24,25]

for pg_num in range(1,50+1):

    #Go to next page
    driver.get(f'https://www.maltatoday.com.mt/news/national/{pg_num}/')
    
    #Get list of article links
    all_links = driver.find_elements(By.CLASS_NAME,'news-article')
    links = [all_links[i].get_attribute('data-url') for i in idx_lst]

    for a in links:
        
        #Go to next article
        driver.get(f'https://www.maltatoday.com.mt/{a}')
        
        #Get title
        title = driver.find_element(By.XPATH,'//*[@id="content"]/section/div/div[1]/div/div/div[2]/div/div/div/h1').text

        #Get Body
        try:    text_content = driver.find_element(By.CLASS_NAME,'content-news')
        except: 
            try: text_content = driver.find_element(By.CLASS_NAME,'content-announcements')
            except: continue #If other, skip article
        
        body = " ".join(p.text for p in text_content.find_elements(By.TAG_NAME,'p'))


        #Get links to all images+thumbnail in the article
        img_links = [i.find_element(By.TAG_NAME,'img') for i in 
                            driver.find_elements(By.CLASS_NAME,'cover-photo') + \
                            driver.find_elements(By.CLASS_NAME,'photo-item')]
                                 
        captions = ""
        images   = ""

        #Write images to disk
        for img_link in img_links:
            img_src   = img_link.get_attribute('src')        #Get source
            captions  += img_link.get_attribute('alt') + '☺' #Append current caption

            img_ext  = get_img_ext(img_src)                    #Get image extension
            img_name = f'img{str(img_count).zfill(5)}'+img_ext #Get image name
            images  += img_name + ','                          #Append image name to list
            img_data = requests.get(img_src).content           #Download image

            img_count += 1

            #Write current image to disk
            with open(os.path.join(m.NEWS_IMG_PATH,img_name),'wb') as f:
                f.write(img_data)

        data.append([title,images[:-1],captions[:-1],body])

pd.DataFrame(columns=['Title','Image Name','Caption','Body'],
             data=data).to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)

    

    


