import os
import sys
import signal
import requests
import selenium
import pandas as pd
from time import sleep
from methods import WebScraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

m = WebScraper(folder_name='times_of_malta')

def signal_handler(sig,frame):
    pd.DataFrame(columns=['Title','Image Name','Caption','Body'],
            data=data).to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)
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

# Since chromedriver is in PATH we dont have specify it location otherwise webdriver.Chrome('path/chromedriver.exe')
driver = webdriver.Chrome(m.CHROME_DRIVER_PATH, options=options)

# Opening required website to scrape content 
driver.get('https://timesofmalta.com/articles/tags/national')


#Closing pop-ups
print('Closing initial pop-ups: ',end='')
driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div[1]/div[2]/div[2]/button[1]').click()
print('[OK]')


data = []
count = 0
article_index = 0
page_index = 0

#Setup ^C Handler to save on signal.

for i in range(2500):

    signal.signal(signal.SIGINT, signal_handler)

    try: 
        #Remove donation message
        try: driver.find_element(By.XPATH,'//*[@id="eng-accept"]').click()
        except: pass
                
        #Click on article
        driver.find_element(By.XPATH,f'//*[@id="listing-articles"]/div[{str(2+article_index)}]/a').click()
       
        #Increment article index
        article_index += 1

        sleep(0.5)
        #Get Title
        title = driver.find_element(By.XPATH,'//*[@id="article-head"]/div/h1').text

        print(f'Title: {title}')
        
        #Get Thumbnail + Images
        img_links = [img for img in \
                     driver.find_elements(By.XPATH,'//*[@id="observer"]/main/article/div[2]/div/*/img') +\
                     driver.find_elements(By.XPATH,'//*[@id="article-head"]/div/picture/img')]
        
        captions = ""
        images   = ""

        #Write images to disk
        for img_link in img_links:
            img_src   = img_link.get_attribute('src')        #Get source
            captions  += img_link.get_attribute('alt') + '☺' #Append current caption

            img_ext  = get_img_ext(img_src)                #Get image extension
            img_name = f'img{str(count).zfill(5)}'+img_ext #Get image name
            images  += img_name + ','                      #Append image name to list
            img_data = requests.get(img_src).content       #Download image

            count += 1

            #Write current image to disk
            with open(os.path.join(m.NEWS_IMG_PATH,img_name),'wb') as f:
                f.write(img_data)

        # Get Body
        text_content = driver.find_element(By.XPATH,'//*[@id="observer"]/main/article/div[2]/div')                                                     
        body = " ".join(p.text for p in text_content.find_elements(By.TAG_NAME,'p'))

        #Add row
        data.append([title, images[:-1], captions[:-1], body])

        #Save to csv
        if i%50 == 0:
            print('Saving...\n')
            pd.DataFrame(columns=['Title','Image Name','Caption','Body'],
                         data=data).to_csv(os.path.join(m.NEWS_PATH,'data2.csv'), index=False)

    #Go back
        print('Back to home page\n')
        driver.back()

    except selenium.common.exceptions.NoSuchElementException as e:
        #Switch to next page
        sleep(1.5)

        try: driver.find_element(By.XPATH,f'//*[@id="observer"]/main/div/div[2]/div/span[{str(2+page_index)}]').click()
        except: 
            print(f'Error: Reloading page {page_index+2}')
            driver.get(f'https://google.com')
            sleep(2)
            page_index += 1
            driver.get(f'https://timesofmalta.com/articles/tags/national/page:{str(page_index+2)}') #Skip page

            try: driver.find_element(By.XPATH,'//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click() #Close pop-up
            except: pass

            article_index = 0 #Invoke next-page switch
            
            continue #Go back to beggining

        

        page_index   += 1
        article_index = 0
        print(f'Next Page! -> {page_index+1}')
    
    except selenium.common.exceptions.ElementClickInterceptedException as e:
        print('Click Intercepted - Skipping')
        article_index += 1
        continue

    except Exception as e:
        print(str(e))
        article_index += 1
        page_index += 1
        continue

        



# #all XPaths are preceded by the double slash, which we want in a td tag, with each class in that td tag needing to correspond to “name”.
# # titles = driver.find_elements("xpath", '//h2')
# sleep(1000)
# print(titles)

# # Storing all article titles 
# df = pd.DataFrame(columns=['Name(Malti)','Name(Eng)']) # creates master dataframe 

# article_list = []
# article_list_translated = []

# counter = 0
# for p in titles:
#     transText = translator.translate(titles[counter].text, dest='en', src='mt').text
#     article_list.append(titles[counter].text)
#     article_list_translated.append(transText)
#     counter += 1
    
# data_tuples = list(zip(article_list[1:],article_list_translated[1:])) # list of each players name and salary paired together
# temp_df = pd.DataFrame(data_tuples, columns=['Name(Malti)','Name(Eng)']) # creates dataframe of each tuple in list
# df = df.append(temp_df) # appends to master dataframe

# print(counter)
# df.to_csv('testing.csv', index=True)

# # Closing driver when no longer required 
# driver.close()

# for x in range(counter):
#     print(article_list[x], "--", article_list_translated[x])