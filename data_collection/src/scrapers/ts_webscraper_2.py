import re
import os
import sys
import signal
import requests
import xmltodict
import pandas as pd
from lxml import html
from tqdm import tqdm
from time import time, sleep
from ws_methods import WebScraper

m = WebScraper(folder_name='the_shift')

def signal_handler(sig,frame):
    print('SIG Received - Saving..')
    pd.DataFrame(columns=columns,
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

count = 0
data = []
save_every = 50

signal.signal(signal.SIGINT, signal_handler) 

columns = ['Title','Author','Date','Image Name','Caption','Body','URL']
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}


article_urls = [d['loc'] for i in [1,2,3,4] for d in xmltodict.parse(requests.get(f"https://theshiftnews.com/wp-sitemap-posts-post-{i}.xml",
                                                                                  headers=headers).content)['urlset']['url']]

#error on 871
for a in tqdm(article_urls):
    content = requests.get(a,headers=headers).content.decode('utf-8')
    tree = html.fromstring(content)
    
    #Skip Maltese Articles
    if tree.xpath('//*[@id="container"]/div[4]/p[1]/em'):
        continue

    title = tree.xpath('//*[@id="container"]/h2')[0].text

    #Get Caption (if any)
    if c:=tree.xpath('//*[@id="container"]/div[1]/div/p'):
        caption = c[0].text
    else: caption = ""
    
    #Get Body
    body = ' '.join([b.text for b in tree.xpath('//*[@id="container"]/div[4]/p') if type(b.text) == str])

    #Get Author
    author = tree.xpath('//*[@id="container"]/div[2]/div/div[2]/div/a')[0].text

    #Get Date
    match = re.match(r"https:\/\/theshiftnews\.com\/([0-9]*)\/([0-9]*)\/([0-9]*)",a)
    date = f"{match.group(3)}-{match.group(2)}-{match.group(1)}"

    #Get Image
    img_link = tree.xpath('//*[@id="container"]/div[1]/div/img')[0].attrib['src']
    img_ext = get_img_ext(img_link)        
    img_name = f'img{str(count).zfill(5)}' + img_ext #Get image name
    count += 1
    
    #Skip if no image
    if img_link == '':
        continue

    #Download Image
    while len(img_data := requests.get(img_link,headers=headers).content) <= 146: pass
    with open(os.path.join(m.NEWS_IMG_PATH,img_name),'wb') as f:
        f.write(img_data)

    #Add row
    data.append([title,author,date,img_name,caption,body,a])
    
    #Save to csv
    if count%save_every == 0:
        (pd.DataFrame(columns=columns,data=data)
            .to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)) 
        
(pd.DataFrame(columns=columns,data=data)
            .to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)) 






