import os
import pandas as pd

data_path = os.path.join('..','times_of_malta')

df = pd.read_csv(os.path.join(data_path,'blip_data.csv'),
                 nrows=800, index_col=False)

df = df[df['Title'].map(lambda x: not str(x).startswith("Today's front pages"))]

df['NER Caption'] = df['NER Caption'].apply(lambda x: None if str(x).strip() in
                                            ["File photo","File photo.","File photo: Organisation",
                                            "File photo: Person","File Photo: Person",
                                            "File Photo: Organisation", "Photo: Person"] else x)


df.to_csv(os.path.join(data_path,'blip_data.csv'),
          columns=['Title','NER Title','Title s_Positive','Title s_Neutral','Title s_Negative','Image Name','Caption','NER Caption','BLIP Caption','Caption s_Positive','Caption s_Neutral','Caption s_Negative','Body','NER Body','KW Body','Body s_Positive','Body s_Neutral','Body s_Negative'],
          index=False)

"File photo"