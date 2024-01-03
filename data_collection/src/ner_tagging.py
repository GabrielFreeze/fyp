import os
import sys
import pandas as pd
from time import time
from methods import NERTagger

def main(folder:str):

    tagger = NERTagger()
    columns=['Title','NER Title','Image Name','Body','NER Body']
    print('STARTING')
    data_path = os.path.join('..',folder)
    

    df = pd.read_csv(os.path.join(data_path,'data.csv'),
                    nrows=800, index_col=False)

    start = time()
    print('NER-Switching Title: ')
    df['NER Title'] = df['Title'].apply(lambda s: tagger.ner_switch(str(s)))
    print(f'[OK] - {round(time()-start,2)}')


    if 'Caption' in df.columns:
        
        columns = columns[:3]+['Caption','NER Caption']+columns[3:]

        start = time()
        print('NER-Switching Caption: ')
        df['NER Caption'] = df['Caption'].apply(lambda s: tagger.ner_switch(str(s)) if s else None)
        print(f'[OK] - {round(time()-start,2)}')

        

    start = time()
    print('NER-Switching Body: ')
    df['NER Body'] = df['Body'].apply(lambda s: tagger.ner_switch(str(s)))
    print(f'[OK] - {round(time()-start,2)}')

    df.to_csv(os.path.join(data_path,'ner_data.csv'),
              columns=columns,index=False)


if __name__ == '__main__':

    main(folder=sys.argv[1])

























