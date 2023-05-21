import os
import pandas as pd
from time import time
from methods import NERTagger

def main():

    tagger = NERTagger()
    print('STARTING')
    data_path = os.path.join('..','malta_daily')
    

    df = pd.read_csv(os.path.join(data_path,'data.csv'),
                    nrows=800, index_col=False)

    start = time()
    print('NER-Switching Title: ')
    df['NER Title'] = df['Title'].apply(lambda s: tagger.ner_switch(str(s)))
    print(f'[OK] - {round(time()-start,2)}')

    start = time()
    print('NER-Switching Caption: ')
    df['NER Caption'] = df['Caption'].apply(lambda s: tagger.ner_switch(str(s)) if s else None)
    print(f'[OK] - {round(time()-start,2)}')

    start = time()
    print('NER-Switching Body: ')
    df['NER Body'] = df['Body'].apply(lambda s: tagger.ner_switch(str(s)))
    print(f'[OK] - {round(time()-start,2)}')

    df.to_csv(os.path.join(data_path,'ner_data.csv'),
            columns=['Title','NER Title','Image Name','Caption','NER Caption','Body','NER Body'],
            # columns=['Title','NER Title','Image Name','Body','NER Body'],
            index=False)


if __name__ == '__main__':
    main()

























