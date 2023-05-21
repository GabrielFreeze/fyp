import os
import re
import numpy as np
from time import time
from typing import Tuple

# from keybert import KeyBERT
# from flair.data import Sentence
# from flair.models import SequenceTagger
from NewsSentiment import TargetSentimentClassifier


class WebScraper:

    def __init__(self,folder_name='data'):
        self.CHROME_DRIVER_PATH = os.path.join('..','chromedriver_win32',
                                               'chromedriver_win32.exe')
        self.GECKO_DRIVER_PATH  = os.path.join('..','geckodriver')
                                               
        self.NEWS_IMG_PATH = os.path.join('..',folder_name,'img')
        self.NEWS_PATH = os.path.join('..',folder_name)

def init_directory(self, subs):

    #Ensures that all folders relating to subreddits
    #are already created in the folder images.
    for sub in subs:
        if not os.path.exists(f'sub\\{sub}'):
            os.mkdir(f'sub\\{sub}')
        if not os.path.exists(f'sub\\{sub}\\images'):
            os.mkdir(f'sub\\{sub}\\images')
    
    return

class NERTagger:
    def __init__(self, ner_path=os.path.join('..','..','checkpoints','flair_ner_english')) -> None:
        self.tagger = SequenceTagger.load(ner_path)
        self.counter = 0
        
        self.tag2str = {'PER':'Person',
                        'LOC':'Location',
                        'ORG':'Organisation'}
        
        self.locations = {"Żurrieq","Zurrieq","Gozo","Malta","Zejtun","Zebbug","Zabbar","Xghajr",
                          "Żejtun","Żebbuġ","Żebbuġ","Żabbar","Xgħajr","Xewkija","Xagħra","Xaghra",
                          "Victoria","Valletta","Tarxien","Ta' Xbiex","Swieqi","St. Paul's Bay",
                          "St. Julian's","Sliema","Siġġiewi","Siggiewi","Senglea","Isla",
                          "Santa Venera","Santa Luċija","Santa Lucija","Sannat","San Lawrenz",
                          "San Ġwann","San Gwann","Safi","Rabat","Qrendi","Qormi","Qala","Pietà",
                          "Pieta","Pembroke","Paola","Naxxar","Nadur","Munxar","Mtarfa","Msida",
                          "Mqabba","Mosta","Mġarr","Mgarr","Imgarr","Imġarr","Mellieħa","Mellieha",
                          "Mdina","Marsaxlokk","Marsaskala","Marsascala","Marsa","Luqa","Lija","Kirkop",
                          "Kerċem","Kercem","Kalkara","Iklin","Ħamrun","Hamrun","Gżira","Gzira","Gudja",
                          "Għaxaq","Ghaxaq","Gharghur","Għargħur","Għarb","Gharb","Għajnsielem","Ghajnsielem",
                          "Fontana","Floriana","Fgura","Dingli","Cospicua","Bormla","Birżebbuġa","Birzebbuga",
                          "Birkirkara","Birgu","Balzan","Attard"}
     
    def ner_switch(self, raw_str:str) -> str:     
        
        self.counter += 1
        print(f'{round((self.counter/800)*100,2)}%',end='\r')

        #Replace ambiguous location names with Tokyo,
        #which will get flagged as LOC

        for loc in self.locations:
            raw_str = raw_str.replace(loc,'Tokyo')
            raw_str = raw_str.replace(loc.lower(),'Tokyo')

        ner_str = raw_str

        sentence = Sentence(raw_str)
        
        # predict NER tags
        self.tagger.predict(sentence)

        delta_len = 0

        #Switch contextual information with NER tag
        for entity in sentence.get_spans('ner'):
            s   = entity.start_position + delta_len
            e   = entity.end_position   + delta_len
            
            ner = entity.get_label("ner").value

            #Do not include MISC tags
            if ner == 'MISC':
                continue

            #Change NER tag if in tag2str
            if ner in self.tag2str:
                ner = self.tag2str[ner]

            this_len = len(ner_str)
            ner_str = ner_str[:s] + ner + ner_str[e:]

            delta_len += len(ner_str) - this_len
        


        return ner_str

class KeyWordExtractor:
    def __init__(self):
        self.model = KeyBERT()
        self.counter = 0
    
    def extract_keywords(self, raw_str:str)->str:
        self.counter += 1
        print(f'{round((self.counter/800)*100,2)}%',end='\r')
        keywords  = self.model.extract_keywords(docs=raw_str,
                                     top_n=20, keyphrase_ngram_range=(1,1))
        keywords += self.model.extract_keywords(docs=raw_str,
                                     top_n=5, keyphrase_ngram_range=(1,2))
        
        return ",".join([kw for kw,_ in keywords])            

class SentimentAnalysis:
    def __init__(self):
        self.tsc = TargetSentimentClassifier()
        self.counter = 0
    
    def get_sentiment(self, raw_str) -> Tuple[float,float,float]:
        
        # self.counter += 1
        # print(f'{round((self.counter/800)*100,2)}%',end='\r')


        if type(raw_str) is list:
            raw_str = '. '.join(raw_str)
        
        raw_str = raw_str.strip()
        raw_str = raw_str.replace('☺',',')

        #Skip if length of sentence exceeds model input
        if len(raw_str) >= 512 or raw_str == '' or raw_str == 'nan':
            return 0.0,0.0,0.0

        
        print(f'\n{raw_str}\n')
        
        pos = 0
        net = 0
        neg = 0
        
        div = [1,2,2]
        j = 0

        for key in ['Person','Organisation','Location']:
            
            #Calculates TSC on every instance of the key in the title.
            sentiment = [(self.tsc.infer_from_text(raw_str[:w.start()],raw_str[w.start():w.end()],raw_str[w.end():])) \
                        for w in re.finditer(key, raw_str)]
            
            #If key is not in title, skip.
            if not sentiment: continue

            #Get current average score for each sentiment
            pos += sum([self.tsc.get_info_for_label(s,'positive')['class_prob'] for s in sentiment])/len(sentiment)
            net += sum([self.tsc.get_info_for_label(s,'neutral' )['class_prob'] for s in sentiment])/len(sentiment)
            neg += sum([self.tsc.get_info_for_label(s,'negative')['class_prob'] for s in sentiment])/len(sentiment)

            #Divide to average over all results.
            pos /= div[j]
            net /= div[j]
            neg /= div[j]
            
            #Increment total divisor counter
            j += 1

        #If no key was found in title, perform TSC on entire title and add to respective list.
        if j == 0:
            s = self.tsc.infer_from_text("",raw_str,"")

            pos = self.tsc.get_info_for_label(s,'positive')['class_prob']
            net = self.tsc.get_info_for_label(s,'neutral' )['class_prob']
            neg = self.tsc.get_info_for_label(s,'negative')['class_prob']
        
        return round(pos,4), round(net,4), round(neg,4)
    
    def get_custom_sentiment(self, raw_str:str, key:str) -> Tuple[float,float,float]:
        
        self.counter += 1
        print(f'{round((self.counter/800)*100,2)}%',end='\r')

        #Skip if length of sentence exceeds model input or invalid string
        if raw_str == ''       or \
           raw_str == 'nan'    or \
           key not in raw_str:
            return 0.0,0.0,0.0


        sentiment = []

        #Calculates TSC on every instance of the key in the title.
        if len(raw_str) > 512:
            
            for sentence in get_sentences(raw_str):
                
                try:
                    sentiment.extend((self.tsc.infer_from_text(sentence[:w.start()],
                                                            sentence[w.start():w.end()],
                                                            sentence[w.end():]))
                                    for w in re.finditer(key, sentence))
                except: pass
                    

        else:            
            sentiment = [(self.tsc.infer_from_text(raw_str[:w.start()],
                                                raw_str[w.start():w.end()],
                                                raw_str[w.end():]))
                        for w in re.finditer(key, raw_str)]
        
        #Get sentiment scores
        pos = np.mean([self.tsc.get_info_for_label(s,'positive')['class_prob'] for s in sentiment])
        net = np.mean([self.tsc.get_info_for_label(s,'neutral' )['class_prob'] for s in sentiment])
        neg = np.mean([self.tsc.get_info_for_label(s,'negative')['class_prob'] for s in sentiment])
        
        return round(pos,4), round(net,4), round(neg,4)


def get_sentences(text:str):
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    digits = "([0-9])"


    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    
    return [s.strip() for s in sentences]

    

def get_1st_last_sentence(text:str):
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    digits = "([0-9])"


    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    

    try: sen = [sentences[0],sentences[-1]]
    except: return ''
    
    sen = [s.strip() for s in sen]

    x = ' '.join(sen)

    return x
