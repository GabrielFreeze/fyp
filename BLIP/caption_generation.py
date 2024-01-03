import os
import sys
import torch
import pandas as pd
from PIL import Image
from time import time
from torchvision import transforms
from models.blip import blip_decoder
from torchvision.transforms.functional import InterpolationMode

img_sz = 640
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_demo_image(img_path, img_sz, scl=3):
    
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

    def get_gencap(imgs: str) ->  str:
        captions = []

        for img_str in imgs.split(','):
            s = time()
            
            #Perform inference
            img = load_demo_image(img_path=os.path.join(data_path,'img',img_str),
                                  img_sz=img_sz)
            
            with torch.no_grad(): #TODO: Bug Fix here
                caption = model.generate(img, sample=False, top_p=0.9, max_length=20, min_length=5) 
            
            print(f'{time()-s}s: {caption}')
            captions += caption
        
        return '☺'.join(captions)
    
    if not os.path.isfile(pretrained_path:=os.path.join('..','checkpoints','blip_base.pth')):
        pretrained_path = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_capfilt_large.pth'

    model = blip_decoder(pretrained=pretrained_path, image_size=img_sz, vit='base')
    model.eval()
    model = model.to(device)

    data_path = os.path.join('..','data_collection',data_path) #Bad Practice?

    #Read dataframe
    df = pd.read_csv(os.path.join(data_path,'kw_data.csv'), nrows=800)

    columns=['Title','NER Title','Image Name','BLIP Caption','Body','NER Body','KW Body']
    
    if 'Caption' in df.columns:
        columns = columns[:6]+['Caption','NER Caption']+columns[6:]

    #Produce generated captions 
    df['BLIP Caption'] = df['Image Name'].apply(lambda s: get_gencap(str(s)))


    df.to_csv(os.path.join(data_path,'blip_data.csv'),
              columns=columns,index=False)

        
if __name__ == '__main__':
    main(sys.argv[1])