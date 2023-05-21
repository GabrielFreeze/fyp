import os
import signal
import sys
from time import sleep, time

import numpy as np
import pandas as pd
import requests
import selenium
from methods import WebScraper
from selenium import webdriver
from selenium.webdriver.common.by import By

m = WebScraper(folder_name='the_shift')

def signal_handler(sig,frame):
    
    pd.DataFrame(columns=['Title','Image Name','Category','Caption','Body'],
                         data=data).to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)
    driver.quit()
    sys.exit()

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_extension(os.path.join('..','chromedriver_win32','uBlock-Origin.crx'))
# options.add_experimental_option('excludeSwitches', ['enable-logging'])

# # Since chromedriver is in PATH we dont have specify it location otherwise webdriver.Chrome('path/chromedriver.exe')
driver = webdriver.Chrome(m.CHROME_DRIVER_PATH, chrome_options=options)


def remove_dono():
    #Remove occasional donation pop-up (great ux btw)
    try: driver.find_element(By.XPATH,'//*[@id="popmake-64842"]/button')
    except: pass
def get_img_ext(img_link):

    if img_link.endswith('.jpeg'):
        return '.jpeg'
    elif img_link.endswith('.jpg'):
        return '.jpg'
    elif img_link.endswith('.png'):
        return '.png'
    else: return ""


#Wait for donation pop-up to appear and close it forever
driver.get(f'https://theshiftnews.com/2022/01/08')
sleep(5)
remove_dono()
count = 624
data = []
try:
    for pg_num in range(22,50+1):
        
        #Go to next page
        driver.get(f'https://theshiftnews.com/category/news/page/{pg_num+1}/')

        #Get list of articles
        links = [i.find_element(By.TAG_NAME,'a').get_attribute('href') 
                for i in driver.find_elements(By.CLASS_NAME,'comitem')]
        
        for a in links:
            #Go to article
            driver.get(a)
            remove_dono()

            #Go to english article if available
            if driver.find_elements(By.XPATH,'//*[@id="container"]/div[4]')[0].text\
                .startswith('This article is available'):
                remove_dono()
                driver.get(driver.find_element(By.XPATH,'//*[@id="container"]/div[4]/p[1]/em/a')\
                           .get_attribute('href'))
                print('Redirecting to English article.')

            
            #Get title
            title = driver.find_element(By.XPATH,'//*[@id="container"]/h2').text

            #Get caption if any
            try: caption = driver.find_element(By.XPATH,'//*[@id="container"]/div[1]/div/p').text
            except: caption = ""
            
            #Get body
            body = driver.find_element(By.XPATH,'//*[@id="container"]/div[4]').text

            remove_dono()

            #Get image
            img_link = driver.find_element(By.XPATH,'//*[@id="container"]/div[1]/div/img').get_attribute('src')
            img_ext = get_img_ext(img_link)        
            img_name = f'img{str(count).zfill(5)}' + img_ext #Get image name
            count += 1
            
            #Ensure the image actually downloads
            while len(img_data := requests.get(img_link).content) <= 146: pass

            remove_dono()


            with open(os.path.join(m.NEWS_IMG_PATH,img_name),'wb') as f:
                f.write(img_data)

            data.append([title,img_name,caption,body])
            print(count,pg_num)
except Exception as e: print(str(e))
    
pd.DataFrame(data,columns=['Title','Image Name','Caption','Body'])\
    .to_csv(os.path.join(m.NEWS_PATH,'data.csv'),index=False, mode='a', header=False)

            
        


    

    























# #For all specified dates
# for i,d in enumerate(dates):
#     try:
        
#         remove_dono()

#         #Open article page for that date
#         try: driver.get(f'https://theshiftnews.com/{d}')
#         except: continue

#         sleep(0.3)
#         remove_dono()
        
#         #List Comprehension might be redundant?
#         num_articles = len([article.find_element(By.TAG_NAME,'a') for article in driver.find_elements(By.CLASS_NAME,'conitem')])
        
#         #Loop through all articles of current date
#         for j in range(num_articles):
#             print(str(count).zfill(5))

#             remove_dono()

#             start = time()
#             print('Clicking Link - ',end='')
            
#             try: driver.find_elements(By.CLASS_NAME,'conitem')[j].find_element(By.TAG_NAME,'a').click()
#             except:
#                 sleep(1)
#                 remove_dono()
#                 driver.find_elements(By.CLASS_NAME,'conitem')[j].find_element(By.TAG_NAME,'a').click()
            
#             driver.set_window_size(400, 800)
#             driver.set_window_size(960, 1080)
            
#             remove_dono()

#             #Get title
#             print('Title - ',end='')
#             title = driver.find_element(By.XPATH,'//*[@id="container"]/h2').text

#             #Get caption (if any)
#             print('Caption - ',end='')
#             try: caption = driver.find_element(By.XPATH,'//*[@id="container"]/div[1]/div/p').text
#             except: caption = None

#             #Get category
#             print('Category - ',end='')
#             category = driver.find_element(By.XPATH,'//*[@id="container"]/div[1]/div/div').text

#             #Get body
#             print('Body - ',end='')
#             body = driver.find_element(By.XPATH,'//*[@id="container"]/div[4]').text
            
#             #Get image
#             print('Image')
#             img_link = driver.find_element(By.XPATH,'//*[@id="container"]/div[1]/div/img').get_attribute('src')

#             if img_link.endswith('.jpeg'):
#                 img_ext = '.jpeg'
#             elif img_link.endswith('.jpg'):
#                 img_ext = '.jpg'
#             elif img_link.endswith('.png'):
#                 img_ext = '.png'
#             else:
#                 print('Skipping Article')
#                 driver.get(f'https://theshiftnews.com/{d}')
#                 continue
            
#             img_name = f'img{str(count).zfill(5)}' + img_ext #Get image name
            
#             #Ensure the image actually downloads
#             while len(img_data := requests.get(img_link).content) <= 146: pass

#             with open(os.path.join(m.NEWS_IMG_PATH,img_name),'wb') as f:
#                 f.write(img_data)

#             #Save data
#             data.append([title, img_name, category, caption, body])

#             #Go back
#             driver.get(f'https://theshiftnews.com/{d}')
#             sleep(0.5)

            
#             pd.DataFrame(columns=['Title','Image Name','Category','Caption','Body'],
#                         data=data).to_csv(os.path.join(m.NEWS_PATH,'data.csv'),
#                         mode='a',index=False, header=False)
#             data = []

#             count += 1
#     except Exception as e:
#         print(str(e))
#         pass
# # driver.get('https://timesofmalta.com/articles/tags/national')





