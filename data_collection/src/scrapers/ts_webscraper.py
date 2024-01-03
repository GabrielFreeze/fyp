import os
import re
import requests
import pandas as pd
from time import time
from time import sleep
from ws_methods import WebScraper
from selenium import webdriver
from selenium.webdriver.common.by import By

m = WebScraper(folder_name='the_shift')

# def signal_handler(sig,frame):
#     print('SIG Received - Saving..')
#     pd.DataFrame(columns=columns,
#             data=data).to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)
#     driver.quit()
#     sys.exit()
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

# Since chromedriver is in PATH we dont have specify it location otherwise webdriver.Chrome('path/chromedriver.exe')
driver = webdriver.Chrome(m.CHROME_DRIVER_PATH)
count = 0
data = []

num_pgs = 100
save_every = 5
assert num_pgs%save_every == 0

columns = ['Title','Author','Date','Image Name','Caption','Body','URL']


driver.get(f'https://theshiftnews.com/2022/01/08')
sleep(5)

#Accept Cookies
try: driver.find_element(By.XPATH,'//*[@id="cookie_action_close_header"]').click()
except: pass

#Close Donation pop-up
remove_dono()



for pg_idx in range(num_pgs+1):
    print(f'Page: {pg_idx+1}')
    #^C Handler to save on signal.
    # signal.signal(signal.SIGINT, signal_handler) 

    #Go to (next) page
    driver.get(f'https://theshiftnews.com/category/news/page/{pg_idx+1}/')

    #Get list of articles
    links = [i.find_element(By.TAG_NAME,'a').get_attribute('href') 
            for i in driver.find_elements(By.CLASS_NAME,'comitem')]
    
    for a in links:
        #Go to article
        driver.get(a)

        try:

            #Go to english article if available
            if (driver.find_elements(By.XPATH,'//*[@id="container"]/div[4]')[0].text.startswith('This article is available')):
                driver.get((driver.find_element(By.XPATH,'//*[@id="container"]/div[4]/p[1]/em/a')
                                .get_attribute('href')))
            
            #Get Title
            title = driver.find_element(By.XPATH,'//*[@id="container"]/h2').text
            print(f'Extracting: {title[:30]}... ',end='')

            #Get Caption (if any)
            try: caption = driver.find_element(By.XPATH,'//*[@id="container"]/div[1]/div/p').text
            except: caption = ""
            
            #Get Body
            body = driver.find_element(By.XPATH,'//*[@id="container"]/div[4]').text

            #Get Author
            author = driver.find_element(By.XPATH,'//*[@id="container"]/div[2]/div/div[2]/div/a').text

            #Get URL
            url = driver.current_url

            #Get Date
            match = re.match(r"https:\/\/theshiftnews\.com\/([0-9]*)\/([0-9]*)\/([0-9]*)",url)
            date = f"{match.group(3)}-{match.group(2)}-{match.group(1)}" 

            #Get image
            img_link = driver.find_element(By.XPATH,'//*[@id="container"]/div[1]/div/img').get_attribute('src')
            img_ext = get_img_ext(img_link)        
            img_name = f'img{str(count).zfill(5)}' + img_ext #Get image name
            count += 1
            
            #Ensure the image actually downloads
            t=time()
            while len(img_data := requests.get(img_link).content) <= 146 and time()-t < 5: 
                pass

            with open(os.path.join(m.NEWS_IMG_PATH,img_name),'wb') as f:
                f.write(img_data)
            
            #Add row
            data.append([title,author,date,img_name,caption,body,url])
            print('[OK]')

        except Exception as e:
            print(f'[ERR]')

    #Save to csv
    if pg_idx%save_every == 0:
        print('\nSaving...')
        (pd.DataFrame(columns=columns,data=data)
            .to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)) 


            
        


    

    























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





