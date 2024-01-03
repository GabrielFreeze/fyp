from keybert import KeyBERT

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