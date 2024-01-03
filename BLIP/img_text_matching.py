import os
import sys
import torch
import pandas as pd
from PIL import Image
from time import time
from numpy import mean
from torchvision import transforms
from models.blip_itm import blip_itm
from torch.nn.functional import softmax
from torchvision.transforms.functional import InterpolationMode

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_img(img_path, img_sz, scl=3):   
    raw_image = Image.open(img_path).convert('RGB')
    w,h = raw_image.size
    
    transform = transforms.Compose([
        transforms.Resize((img_sz,img_sz),interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        ]) 
    image = transform(raw_image).unsqueeze(0).to(device)   
    return image


def main(data_path:str):
    
    img_sz = 640

    if not os.path.isfile(pretrained_path:=os.path.join('..','checkpoints','blip_base.pth')):
        pretrained_path = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_capfilt_large.pth'

    model = blip_itm(pretrained=pretrained_path, image_size=img_sz, vit='base')
    model.eval()
    model = model.to(device)


    data_path = os.path.join('..','data_collection',data_path) #Bad Practice?
    df = pd.read_csv(os.path.join(data_path,'simil_data.csv'))

    #Remove empty image names
    df = df[df['Image Name'].map(lambda x: len(str(x))>=7)]

    if 'Caption' in df.columns:
        t_columns = ['NER Title','NER Caption','KW Body']
        columns   = ['Title','NER Title','BLIP Caption x NER Title','ITM x NER Title','ITC x NER Title',
                     'Image Name','BLIP Caption', 'Caption','NER Caption','BLIP Caption x NER Caption','ITM x NER Caption','ITC x NER Caption',
                     'Body','NER Body','KW Body','BLIP Caption x KW Body','ITM x KW Body','ITC x KW Body']
        
    else:
        t_columns = ['NER Title','NER Caption','KW Body']
        columns   = ['Title','NER Title','BLIP Caption x NER Title','ITM x NER Title','ITC x NER Title',
                     'Image Name','BLIP Caption',
                     'Body','NER Body','KW Body','BLIP Caption x KW Body','ITM x KW Body','ITC x KW Body']

    #Perform ITM on the following pairs
    for t in t_columns:
        
        #Get list of pairs: (image,text) for every article.
        #Many images will be matched to the singular article's title/body
        lst = [((k := str(i).split(',')),str(j).split('☺') if t == 'NER Caption' else [str(j)]*len(k))
            for i,j in zip(df['Image Name'].tolist(),df[t].tolist())]
        
        s=time()
        #Perform ITM on every pair and average the resulting score.
        itm_score = [mean([softmax(model(load_img(os.path.join(data_path,'img',img),img_sz),txt,
                                            match_head='itm'),dim=1)[:,1].detach().cpu().numpy()
                        for img,txt in zip(imgs,txts)])
                    for imgs,txts in lst]
        print(f'{t} ITM Processed: {round(time()-s,2)}s')
        
        s=time()
        itc_score = [mean([model(load_img(os.path.join(data_path,'img',img),img_sz),txt,
                                match_head='itc').detach().cpu().numpy()
                        for img,txt in zip(imgs,txts)])
                    for imgs,txts in lst]
        print(f'{t} ITC Processed: {round(time()-s,2)}s')
        
        df[f'ITM x {t}'] = itm_score
        df[f'ITC x {t}'] = itc_score

    #Write to disk
    df.to_csv(os.path.join(data_path,'final_data.csv'), index=False,
            columns=columns)
    
if __name__ == '__main__':
    main(sys.argv[1])