import os
import sys
import signal
import requests
import pandas as pd
from time import sleep
from methods import WebScraper
from selenium import webdriver
from selenium.webdriver.common.by import By

m = WebScraper(folder_name='gozo_news')

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

# signal.signal(signal.SIGINT, signal_handler)

# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument('--disable-browser-side-navigation')
# driver = webdriver.Chrome(m.CHROME_DRIVER_PATH, chrome_options=options)
driver = webdriver.Firefox(m.GECKO_DRIVER_PATH)

data = []
count = 0

for pg_num in range(134):

    #Go to next page
    driver.get(f'https://gozo.news/page/{pg_num+1}/')

    #Attempt to close ad
    # try: driver.find_element(By.XPATH,'//*[@id="dismiss-button"]').click()
    # except: pass

    #Get list of articles
    links = [i.find_element(By.TAG_NAME,'a').get_attribute('href') 
             for i in driver.find_elements(By.CLASS_NAME,'post-thumbnail')]
    
    for a in links:
        print(f'{round(count/800,4)*100}%',end='\r')
        #Go to article
        driver.get(a)

        #Attempt to close ad
        # try: driver.find_element(By.XPATH,'//*[@id="dismiss-button"]').click()
        # except: pass


        #Get title
        title = driver.find_element(By.XPATH,'//*[@id="page"]/div/div/div/section/div[2]/article/div/h1').text
        
        #Get image
        try: img_src = driver.find_element(By.XPATH,'//*[@id="page"]/div/div/div/section/div[2]/article/div/div[3]/div[1]/p[1]/img').get_attribute('src')
        except: continue
        img_name = f'img{str(count).zfill(5)}{get_img_ext(img_src)}' #Get image name
        img_data = requests.get(img_src).content #Download image
        count += 1

        #Write image
        with open(os.path.join(m.NEWS_IMG_PATH,img_name),'wb') as f:
            f.write(img_data)

        #Get body
        body = " ".join([p.text for p in driver.find_element(By.CLASS_NAME,'entry-inner').find_elements(By.TAG_NAME,'p')])

        data.append([title,img_name,body])

#Save data to csv
pd.DataFrame(columns=['Title','Image Name','Body'],
             data=data).to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)
driver.quit()

