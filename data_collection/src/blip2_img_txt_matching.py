import os
import sys
import torch
import pandas as pd
from time import time
from PIL import Image
from numpy import mean
from torch.nn.functional import softmax
from lavis.models import load_model_and_preprocess


def main(folder:str):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    data_path = os.path.join('..',folder)

    model, vis_processors, _ = load_model_and_preprocess(name="blip2_image_text_matching",
                                                                      model_type="pretrain", is_eval=True,
                                                                      device=device)
    df = pd.read_csv(os.path.join(data_path,'simil_data.csv'))
    df = df[df['Image Name'].map(lambda x: len(str(x))>=7)] #Remove empty image names

    if 'Caption' in df.columns:
        t_columns = ['NER Title','NER Caption','KW Body']
        columns = ['Title','NER Title','BLIP Caption x NER Title','ITM x NER Title','ITC x NER Title',
                   'Image Name','BLIP Caption', 'Caption','NER Caption','BLIP Caption x NER Caption','ITM x NER Caption','ITC x NER Caption',
                   'Body','NER Body','KW Body','BLIP Caption x KW Body','ITM x KW Body','ITC x KW Body']
        
    else:
        t_columns = ['NER Title','KW Body']
        columns = ['Title','NER Title','BLIP Caption x NER Title','ITM x NER Title','ITC x NER Title',
                   'Image Name','BLIP Caption',
                   'Body','NER Body','KW Body','BLIP Caption x KW Body','ITM x KW Body','ITC x KW Body']



    #Perform ITM on the following pairs
    for t in t_columns:
        
        #Get list of pairs: (image,text) for every article.
        #Many images will be matched to the singular article's title/body
        lst = [((k := str(i).split(',')),str(j).split('☺') if t == 'NER Caption' else [str(j)]*len(k))
            for i,j in zip(df['Image Name'].tolist(),df[t].tolist())]
        
        #Calculate ITM score
        s=time()
        itm_score = []
        for imgs,txts in lst:
            scores = []

            for img,txt in zip(imgs,txts):

                img = Image.open(os.path.join(data_path,'img',img)).convert("RGB")
                img = vis_processors["eval"](img).unsqueeze(0).to(device)

                itm_output = model({"image": img, "text_input": txt}, match_head="itm")
                score = softmax(itm_output,dim=1)[:,1].cpu().detach()[0]

                scores.append(score)
            
            itm_score.append(mean(scores))
        
        print(f'{t} ITM Processed: {round(time()-s,2)}s')

        #Calculate ITC score
        s=time()
        itc_score = []
        for imgs,txts in lst:
            scores = []

            for img,txt in zip(imgs,txts):

                img = Image.open(os.path.join(data_path,'img',img)).convert("RGB")
                img = vis_processors["eval"](img).unsqueeze(0).to(device)

                itc_output = model({"image": img, "text_input": txt}, match_head="itc")
                score = itc_output[0][0].detach().cpu()
                scores.append(score)

            itc_score.append(mean(scores))

        print(f'{t} ITC Processed: {round(time()-s,2)}s')
        
        df[f'ITM x {t}'] = itm_score
        df[f'ITC x {t}'] = itc_score

    #Write to disk
    df.to_csv(os.path.join(data_path,'final_data.csv'),
              columns=columns, index=False)
    

if __name__ == '__main__':
    main(sys.argv[1])


    