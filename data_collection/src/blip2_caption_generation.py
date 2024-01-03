import os
import sys
import torch
import pandas as pd
from PIL import Image
from time import time
from lavis.models import load_model_and_preprocess

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def main(folder:str):

    def get_gencap(imgs: str) ->  str:
        captions = []

        for img_str in imgs.split(','):
            s = time()
            #Perform inference
            img = Image.open(os.path.join(data_path,'img',img_str)).convert("RGB")
            img = vis_processors["eval"](img).unsqueeze(0).to(device)

            caption = model.generate({"image": img}, max_length=50, min_length=10)
            
            print(f'{round(time()-s,2)}s: {caption}')
            captions += caption
        
        return '☺'.join(captions)

    data_path = os.path.join('..',folder)
    df = pd.read_csv(os.path.join(data_path,'kw_data.csv'),nrows=800)

    columns=['Title','NER Title','Image Name','BLIP Caption',
             'Body','NER Body','KW Body']
    
    if 'Caption' in df.columns:
        columns = columns[:6]+['Caption','NER Caption']+columns[6:]

    model, vis_processors, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco",
                                                         is_eval=True, device=device)


    #Produce generated captions 
    df['BLIP Caption'] = df['Image Name'].apply(lambda s: get_gencap(str(s)))

    # df['Title s_Positive'  ] = 0
    # df['Title s_Neutral'   ] = 0
    # df['Title s_Negative'  ] = 0
    # df['Caption s_Positive'] = 0
    # df['Caption s_Neutral' ] = 0
    # df['Caption s_Negative'] = 0
    # df['Body s_Positive'   ] = 0
    # df['Body s_Neutral'    ] = 0
    # df['Body s_Negative'   ] = 0 
    
        
    df.to_csv(os.path.join(data_path,'blip_data.csv'),
                        columns=columns,index=False)

    return


if __name__ == '__main__':
    main(folder=sys.argv[1])








