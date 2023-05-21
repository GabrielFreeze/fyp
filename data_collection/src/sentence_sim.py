import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util

data_path = os.path.join('..','independent')
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

df = pd.read_csv(os.path.join(data_path,'blip_data.csv'),
                 nrows=800, index_col=False)

#Perform sentence similarity on the following pairs
for t in ["NER Caption",
          "KW Body", "NER Title"]:
    
    df[f'BLIP Caption x {t}'] = [str(util.pytorch_cos_sim(model.encode(str(i), convert_to_tensor=True),
                                                          model.encode(str(j).replace('☺',','),
                                                                       convert_to_tensor=True)).tolist()[0][0])
                                 for i,j in zip(df["BLIP Caption"].tolist(),df[t].tolist())]

#Write to disk
df.to_csv(os.path.join(data_path,'simil_data.csv'), index=False) 
