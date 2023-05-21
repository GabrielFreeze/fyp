import sys
import praw
import urllib
import signal
import pandas as pd
from methods import init_directory
from psaw import PushshiftAPI


ps = PushshiftAPI()
reddit = praw.Reddit(client_id="ojoi-60847jYlC0X0EC6UQ",
                     client_secret="--2t3RPVNwCWWWj0eKz2FMi8qzhXEg",
                     user_agent="FYP Reddit Scraper")


def signal_handler(sig,frame):
    pd.DataFrame(columns=['id','subreddit','title','author','created_utc','score','upvote_ratio', 'num_comments', 'over_18', 'url', 'img','num'],
            data=subdata).to_csv(f'sub\\{sub}\\data.csv', index=False)
    sys.exit()




subs = ['NatureIsFuckingLit']
subdata = []




#Prepare directory for webscraping
init_directory(subs)

for sub in subs:
    count = 0
    
    for psaw_post in ps.search_submissions(subreddit=sub, limit=25):

        signal.signal(signal.SIGINT, signal_handler)

        #Get PRAW post from PSAW ID
        post = reddit.submission(id=psaw_post.id)

        try:
            
            #Check if post is not removed by moderators.
            if post.removed_by_category is not None:
                print('.', end='\r')
                continue
            
            print(count, end='\r')
            
            row = [post.id, sub, post.title, post.author, post.created_utc, post.score, post.upvote_ratio, post.num_comments, post.over_18, post.url]
                    
            #If the post has an image, save image
            for ext in ['jpg','jpeg','png']:
                
                url = post.url

                #If content is an imgur link
                if 'imgur.com' in url and not url.endswith(ext):
                    url += '.jpg'
                
                #Skip these links
                if 'imgur.com/a/' in url:
                    break
                
                #Download image
                if url.endswith(ext):
                    count += 1
                    img_name = f'sub\\{sub}\\images\\img{str(count).zfill(6)}'
                    urllib.request.urlretrieve(url, f'{img_name}.{ext}')
                    row.append(f'{img_name}.{ext}')
                    row.append(str(count).zfill(6))
                    
                    subdata.append(row)
                    break

        except Exception as e: print('[Fail. Skipping Post]')


    pd.DataFrame(columns=['id','subreddit','title','author','created_utc','score','upvote_ratio', 'num_comments', 'over_18', 'url', 'img','num'],
                data=subdata).to_csv(f'sub\\{sub}\\data.csv', index=False)


    


        
