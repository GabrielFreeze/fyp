import os
import numpy as np
import pandas as pd

columns=['Caption','NER Caption','BLIP Caption x NER Caption','ITM x NER Caption','ITC x NER Caption','Caption s_Positive','Caption s_Neutral','Caption s_Negative']

for n in ['times_of_malta','the_shift','malta_today', 'independent','malta_daily','gozo_news']:
    data_path = os.path.join('..',n,'final_data.csv')
    
    df = pd.read_csv(data_path)
    
    for c in columns:
        if c not in df.columns: df[c] = np.nan

    df.to_csv(data_path,index=False,
              columns=['Title','NER Title','BLIP Caption x NER Title','ITM x NER Title','ITC x NER Title','Title s_Positive','Title s_Neutral','Title s_Negative','Image Name','BLIP Caption','Caption','NER Caption','BLIP Caption x NER Caption','ITM x NER Caption','ITC x NER Caption','Caption s_Positive','Caption s_Neutral','Caption s_Negative','Body','NER Body','KW Body','BLIP Caption x KW Body','ITM x KW Body','ITC x KW Body','Body s_Positive','Body s_Neutral','Body s_Negative'])
    
    
