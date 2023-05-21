import os
import re
from time import time

import pandas as pd
from methods import SentimentAnalysis, get_1st_last_sentence

#https://github.com/fhamborg/NewsMTSC

def main():
    sentiment = SentimentAnalysis()

    # data_path = os.path.join('..','malta_today')
    data_path = os.path.join('..','the_shift')

    df = pd.read_csv(os.path.join(data_path,'final_data.csv'),
                    nrows=800, index_col=False, dtype=object)

    df = df.drop(columns=['Title s_Positive','Title s_Neutral','Title s_Negative',
                          'Caption s_Positive','Caption s_Neutral','Caption s_Negative',
                          'Body s_Positive','Body s_Neutral','Body s_Negative'])
    s = time()
    #Get Sentiment Scores for Title
    df = df.join(pd.DataFrame(df['NER Title'].apply(lambda s: sentiment.get_sentiment(str(s))).tolist(),
                   columns=['Title s_Positive','Title s_Neutral','Title s_Negative']))
    print(f'{time()-s}s')
    

    s = time()
    #Get Sentiment Scores for Caption
    df = df.join(pd.DataFrame(df['NER Caption'].apply(lambda s: sentiment.get_sentiment(str(s)) if s else None).tolist(),
                   columns=['Caption s_Positive','Caption s_Neutral','Caption s_Negative']))
    print(f'{time()-s}s')
    
    s = time()
    #Get Sentiment Scores for Body
    df = df.join(pd.DataFrame(df['NER Body'].apply(
                 lambda s: sentiment.get_sentiment(get_1st_last_sentence(str(s)))).tolist(),
                 columns=['Body s_Positive','Body s_Neutral','Body s_Negative']))
    print(f'{time()-s}s')

        
    df.to_csv(os.path.join(data_path,'final_data.csv'),
            #   columns=['Title','NER Title','Title s_Positive','Title s_Neutral','Title s_Negative',
            #            'Image Name',
            #            'Caption','NER Caption','Caption s_Positive','Caption s_Neutral','Caption s_Negative',
            #            'Body','NER Body','KW Body','Body s_Positive','Body s_Neutral','Body s_Negative'
            #            ],
            columns=['Title','NER Title','BLIP Caption x NER Title','ITM x NER Title','ITC x NER Title','Title s_Positive','Title s_Neutral','Title s_Negative',
                     'Image Name','BLIP Caption','Caption','NER Caption','BLIP Caption x NER Caption','ITM x NER Caption','ITC x NER Caption','Caption s_Positive','Caption s_Neutral','Caption s_Negative',
                     'Body','NER Body','KW Body','BLIP Caption x KW Body','ITM x KW Body','ITC x KW Body','Body s_Positive','Body s_Neutral','Body s_Negative'],
              index=False)
    
if __name__ == '__main__':
    main()




    # t = "Person advocates for Person's rights - Person"


    # print(tsc.get_info_for_label(tsc.infer_from_text("","Person"," advocates for Person's rights - Person"),'neutral')['class_prob'])
    # print(tsc.get_info_for_label(tsc.infer_from_text("Person advocates for Person's rights - ","Person",""),'neutral')['class_prob'])
    # print(tsc.get_info_for_label(tsc.infer_from_text("Person advocates for ","Person","'s rights - Person"),'neutral')['class_prob'])
