import os
import praw
import urllib
import pandas as pd
from methods import Methods
from psaw import PushshiftAPI


subs = ['battlestations']


for sub in subs:

    #Get data.
    df = pd.read_csv(f'sub\\{sub}\\data.csv')
    df = df.dropna()

    #Get all images with a ratio of more than 0.9 and more than 100 upvotes.
    good = df[(df['upvote_ratio'] >= 0.9) & (df['score'] > 100)]

    #Put these images in a seperate folder.
    for i,row in good.iterrows():
        new_path = str(row['img']).replace('images','filtered-images')
        os.rename(row['img'],new_path)

    good.to_csv(f'sub\\{sub}\\filtered.csv', index=False)
