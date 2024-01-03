import os
import re
import sys
import signal
import requests
import pandas as pd
from time import sleep
from selenium import webdriver
from ws_methods import WebScraper
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By

m = WebScraper(folder_name='times_of_malta')

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

driver = webdriver.Chrome(m.CHROME_DRIVER_PATH)

# Opening required website to scrape content 
driver.get('https://timesofmalta.com/articles/tags/national')

#Closing pop-ups
print('Closing initial pop-ups: ',end='')
driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]').click()
print('[OK]')


data = []
img_count = 0
pg_article_sz = 17

num_pgs = 100  # 17 articles per page
save_every = 5
assert num_pgs%save_every == 0

columns = ['Title','Author','Date','Image Name','Caption','Body','URL']

#^C Handler to save on signal.
signal.signal(signal.SIGINT, signal_handler)

for pg_idx in range(num_pgs+1):
    

    #Open (next) page
    driver.get(f"https://timesofmalta.com/articles/listing/national/page:{pg_idx+1}")


    try: 
        #Remove donation message
        try: driver.find_element(By.XPATH,'//*[@id="eng-accept"]').click()
        except: pass

        #Get links to all articles in page
        links = [i.find_element(By.TAG_NAME,'a').get_attribute('href') 
                for i in driver.find_elements(By.CLASS_NAME,"li-ListingArticles_sub")]

        for a in links:
            #Go to article
            driver.get(a)

            #Get Title
            sleep(0.5)
            title = driver.find_element(By.XPATH,'//*[@id="article-head"]/div/h1').text
            print(f'Extracting: {title[:30]}... ',end='')
            
            #Get Author
            try:    author = driver.find_element(By.XPATH,'//*[@id="article-head"]/div/div[2]/div[1]/span[2]/span/a').text
            except: author = driver.find_element(By.XPATH,'//*[@id="article-head"]/div/div[2]/div[1]/span[2]/span').text

            #Get URL
            url = driver.current_url

            #Get Thumbnail + Images
            img_links = [img for img in driver.find_elements(By.XPATH,'//*[@id="observer"]/main/article/div[2]/div/*/img') +\
                                        driver.find_elements(By.XPATH,'//*[@id="article-head"]/div/picture/img')]
            
            captions = ""
            images   = ""

            #Write images to disk
            for img_link in img_links:
                img_src   = img_link.get_attribute('src')         #Get source
                captions  += img_link.get_attribute('alt') + '☺'  #Append current caption

                img_ext  = get_img_ext(img_src)                    #Get image extension
                img_name = f'img{str(img_count).zfill(5)}'+img_ext #Get image name
                images  += img_name + ','                          #Append image name to list
                img_data = requests.get(img_src).content           #Download image

                img_count += 1

                #Write current image to disk
                with open(os.path.join(m.NEWS_IMG_PATH,img_name),'wb') as f:
                    f.write(img_data)

            #Get Body
            text_content = driver.find_element(By.XPATH,'//*[@id="observer"]/main/article/div[2]/div')
            body = " ".join(p.text for p in text_content.find_elements(By.TAG_NAME,'p'))

            #Get Date of Article
            date = driver.find_element(By.XPATH,'//*[@id="article-head"]/div/div[2]/div[1]/span[1]').text

            if 'hour' in date:
                current_hr = datetime.now().hour
                article_hr = re.match(r'(.*) hour(s?) ago',date).group(1)

                date = datetime.now()
                if int(current_hr) < int(article_hr):
                    date -= timedelta(days=1)
            elif 'minute' in date:
                date = datetime.now()
            else:                               #vvv This format is only specific to ChromeDriver
                date = datetime.strptime(date,"%B %d, %Y") 

            date = date.strftime('%d-%m-%Y')
            
            #Add row
            data.append([title,author,date,images[:-1],captions[:-1],body,url])

            print('[OK]')

        #Save to csv
        if pg_idx%save_every == 0:
            print('\nSaving...')
            (pd.DataFrame(columns=columns,data=data)
             .to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)) 

    except Exception as e:
        print(f'[ERR]')

