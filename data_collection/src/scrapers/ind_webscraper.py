import os
import sys
import signal
import requests
import pandas as pd
from time import sleep
from datetime import datetime
from selenium import webdriver
from ws_methods import WebScraper,color
from selenium.webdriver.common.by import By

m = WebScraper(folder_name='independent')

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

driver = webdriver.Chrome(m.CHROME_DRIVER_PATH,service_log_path=os.devnull)

#Load Initial Page and remove cookie pop-up
driver.get(f'https://www.independent.com.mt/local?pg=1')
sleep(2)
try: driver.find_element(By.XPATH,'//*[@id="CybotCookiebotDialogBodyButtonDecline"]').click()
except: pass
data = []
img_count = 0

columns = ['Title','Author','Date','Image Name','Caption','Body','URL']

num_pgs = 100
save_every = 5
assert num_pgs%save_every == 0
signal.signal(signal.SIGINT, signal_handler)

#For all pages
for pg_idx in range(5,num_pgs+1):
    
    #Go to next page
    driver.get(f'https://www.independent.com.mt/local?pg={pg_idx+1}')

    #Get all links to articles
    links = []
    for i in driver.find_elements(By.CLASS_NAME,"image-section"):
        try: a = i.find_element(By.TAG_NAME,'a').get_attribute('href')
        except: continue
        
        links.append(a)

    for a in links:

        #Go to Article
        driver.get(a)

        #Get Title
        title = driver.find_element(By.XPATH,'//*[@id="ctl00_wrapperArticlesWrapper"]/section/div[1]/div[1]/article/h2').text        
        print(f'{color.BLUE}Extracting: {title[:30]}... {color.ESC}',end='')

        #Get links to all images+thumbnail in the article
        img_links = [img.get_attribute('src') for img in \
                     driver.find_elements(By.XPATH,'//*[@id="ctl00_wrapperArticlesWrapper"]/section/div[1]/div[1]/article/div[3]/*/img')+\
                     driver.find_elements(By.XPATH,'//*[@id="ctl00_wrapperArticlesWrapper"]/section/div[1]/div[1]/article/div[2]/img')  +\
                     driver.find_elements(By.XPATH,'//*[@id="ctl00_wrapperArticlesWrapper"]/section/div[1]/div[1]/article/div[3]/img')]  
                                                    
        images = ""

        #Write images to disk
        for img_link in img_links:
            
            img_ext = '.jpeg' #Get Image Extension
            img_name   = f'img{str(img_count).zfill(5)}' + img_ext #Get image name
            img_count += 1
            images    += img_name+',' #Get image names
            img_data   = requests.get(img_link).content #Download image

            #Write image
            with open(os.path.join(m.NEWS_IMG_PATH,img_name),'wb') as f:
                f.write(img_data)
        
        #Get Body
        text_content = driver.find_element(By.CLASS_NAME,'text-container')
        body = " ".join(p.text for p in text_content.find_elements(By.TAG_NAME,'p'))


        #Get Author
        try: author = driver.find_element(By.XPATH,'//*[@id="ctl00_ArticleDetails_TMI_lblAuthor"]').text
        except: author= ""

        #Get Date                           
        date = driver.find_element(By.XPATH,f'//*[@id="ctl00_wrapperArticlesWrapper"]/section/div[1]/div[1]/article/div[1]/span[{[2,1][author==""]}]').text
        date = datetime.strptime(date,"%A, %d %B %Y, %H:%M").strftime('%d-%m-%Y')

        #Append row
        data.append([title,author,date,images[:-1],"",body,a])

    #Save data to csv
    if pg_idx%save_every:
        print(f'Saving on {pg_idx+1}')
        (pd.DataFrame(columns=columns,data=data)
            .to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False))

#Save data to csv
(pd.DataFrame(columns=columns,data=data)
       .to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False))
driver.quit()
