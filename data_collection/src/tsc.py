import os 
import numpy as np
import pandas as pd
from methods import SentimentAnalysis, get_1st_last_sentence



for newspaper in ['times_of_malta','the_shift']:

    data_path = os.path.join('..',newspaper)
    sentiment = SentimentAnalysis()

    #Load data
    df = pd.read_csv(os.path.join(data_path,'final_data.csv'),
                    index_col=False)


    for kw in ['Labour','Nationalist','Minister']:
    
        #Title
        # print(f'{kw} - Title')
        # df = df.join(pd.DataFrame(df['Title'].apply(lambda s: sentiment.get_custom_sentiment(str(s),kw)).tolist(),
        #                 columns=[f'Title s_Positive {kw}',f'Title s_Neutral {kw}',f'Title s_Negative {kw}']))
        
        # #Caption
        # print(f'{kw} - Caption')
        # df = df.join(pd.DataFrame(df['Caption'].apply(lambda s: sentiment.get_custom_sentiment(str(s),kw)).tolist(),
        #                 columns=[f'Caption s_Positive {kw}',f'Caption s_Neutral {kw}',f'Caption s_Negative {kw}']))
        
        #Body
        print(f'{kw} - Body')
        df = df.join(pd.DataFrame(df['Body'].apply(lambda s: sentiment.get_custom_sentiment(str(s),kw)).tolist(),
        columns=[f'Body s_Positive {kw}',f'Body s_Neutral {kw}',f'Body s_Negative {kw}']))


    df.to_csv(os.path.join(data_path,'final_data_tsc.csv'), index=False)

