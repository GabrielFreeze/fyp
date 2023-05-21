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


m = WebScraper(folder_name='independent')

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


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_extension(os.path.join('..','chromedriver_win32','uBlock-Origin.crx'))
# options.add_experimental_option('excludeSwitches', ['enable-logging'])

# # Since chromedriver is in PATH we dont have specify it location otherwise webdriver.Chrome('path/chromedriver.exe')
driver = webdriver.Chrome(m.CHROME_DRIVER_PATH, chrome_options=options)

#Load Initial Page and remove cookie pop-up
driver.get(f'https://www.independent.com.mt/local?pg=1')
sleep(2)
driver.find_element(By.XPATH,'//*[@id="CybotCookiebotDialogBodyButtonDecline"]').click()

data = []
img_count = 0

#For all pages
for pg_num in range(1,100+1):
    #Go to next page
    driver.get(f'https://www.independent.com.mt/local?pg={pg_num}')

    for i in range(9):
        signal.signal(signal.SIGINT, signal_handler)

        #Go to article i
        driver.find_element(By.XPATH,f'//*[@id="ctl00_wrapperArticlesWrapper"]/section/div[1]/div[1]/article[{i+1}]/div[1]/a').click()

        #Get title
        title = driver.find_element(By.XPATH,'//*[@id="ctl00_wrapperArticlesWrapper"]/section/div[1]/div[1]/article/h2').text        
        print(title)

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
                                                       
         
        #Append row
        data.append([title,images[:-1],body])

        #Return to article list
        driver.get(f'https://www.independent.com.mt/local?pg={pg_num}')


#Save data to csv
pd.DataFrame(columns=['Title','Image Name','Body'],
             data=data).to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)
driver.quit()
