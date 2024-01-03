import os
import sys
import signal
import requests
import pandas as pd
from tqdm import tqdm
from time import sleep
from datetime import datetime
from selenium import webdriver
from ws_methods import WebScraper
from selenium.webdriver.common.by import By

m = WebScraper(folder_name='gozo_news')

def signal_handler(sig,frame):
    (pd.DataFrame(columns=columns,data=data)
       .to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False))
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
img_count = 0
num_pgs = 1200
save_every = 5
assert num_pgs%save_every == 0 
columns = ['Title','Author','Date','Image Name','Caption','Body','URL']

for pg_idx in tqdm(range(num_pgs+1)):

    #Go to next page
    driver.get(f'https://gozo.news/page/{pg_idx+1}/')

    #Get list of articles
    links = [i.find_element(By.TAG_NAME,'a').get_attribute('href') 
             for i in driver.find_elements(By.CLASS_NAME,'post-thumbnail')]
    
    for a in links:
        #Go to article
        driver.get(a)

        #Get title
        title = driver.find_element(By.XPATH,'//*[@id="page"]/div/div/div/section/div[2]/article/div/h1').text
        
        #Get image
        try: img_src = driver.find_element(By.XPATH,'//*[@id="page"]/div/div/div/section/div[2]/article/div/div[3]/div[1]/p[1]/img').get_attribute('src')
        except: continue
        img_name = f'img{str(img_count).zfill(5)}{get_img_ext(img_src)}' #Get image name
        img_data = requests.get(img_src).content #Download image
        img_count += 1

        #Write image
        with open(os.path.join(m.NEWS_IMG_PATH,img_name),'wb') as f:
            f.write(img_data)

        #Get body
        body = " ".join([p.text for p in driver.find_element(By.CLASS_NAME,'entry-inner').find_elements(By.TAG_NAME,'p')])

        #Get Author
        author = driver.find_element(By.XPATH,'//*[@id="page"]/div/div/div/section/div[2]/article/div/p/a').text

        #Get Date
        date = driver.find_element(By.XPATH,'//*[@id="page"]/div/div/div/section/div[2]/article/div/p').text.split('·')[1]
        date = datetime.strptime(date," %B %d, %Y").strftime('%d-%m-%Y')

        #Add row
        data.append([title,author,date,img_name,"",body,a])

    if pg_idx%save_every == 0:
        #Save data to csv
        (pd.DataFrame(columns=columns,data=data)
           .to_csv(os.path.join(m.NEWS_PATH,'data.csv'),index=False))        


#Save data to csv
(pd.DataFrame(columns=columns,data=data)
   .to_csv(os.path.join(m.NEWS_PATH,'data.csv'),index=False))
driver.quit()

