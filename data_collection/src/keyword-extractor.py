import os
import pandas as pd
from time import time
from methods import KeyWordExtractor

def main():
    kw_extractor = KeyWordExtractor()
      
    data_path = os.path.join('..','independent')

    df = pd.read_csv(os.path.join(data_path,'ner_data.csv'), index_col=False)

    print('Extracting Keywords from Body:')
    start = time()
    df['KW Body'] = df['NER Body'].apply(lambda s: kw_extractor.extract_keywords(str(s)))
    print(f'[OK] - {round(time()-start,2)}s')

    # print('NER Tagging Keywords:')
    # start=time()
    # df['KW Body'] = df['KW Body'].apply(lambda s: ner_tagger.ner_switch(str(s)))
    # print(f'[OK] - {round(time()-start,2)}s')


    df.to_csv(os.path.join(data_path,'kw_data.csv'),
            columns=['Title','NER Title','Image Name','Caption','NER Caption','Body','NER Body','KW Body'],
            # columns=['Title','NER Title','Image Name','Body','NER Body','KW Body'],
            # columns=['Title','NER Title','Title s_Positive','Title s_Neutral','Title s_Negative','Image Name',
            #          'Caption','NER Caption',
            #         'BLIP Caption',
            #         'Caption s_Positive','Caption s_Neutral','Caption s_Negative',
            #          'Body','NER Body','KW Body','Body s_Positive','Body s_Neutral','Body s_Negative'],
            index=False)


if __name__ == '__main__':
    main()




# keywords = kw_model.extract_keywords(docs=text,
#                                      top_n=5, keyphrase_ngram_range=(2,2))
# for kw,score in keywords:
#     print(f'{kw} - {round(score,2)}')




# from rake_nltk import Rake
# kw_model = Rake(include_repeated_phrases=False,
#                 min_length=1, max_length=1,
#                 punctuations={'.',',','?','!','"','’'})
# # text = """The Organisation will be forcing the government to vote on a public inquiry into the death of 20-year-old Person.  In a statement, Organisation party leader Person said the Opposition will be moving a parliamentary motion that asks for a "public and independent" inquiry into the death of Location.  “Our society needs to send a clear message that something as serious and tragic as this cannot be ignored,” Person said on Tuesday.     Location was the only fatality of a building site collapse on December 3. He was found dead buried beneath the rubble of what was being developed into a timber factory. Five workers were rescued from the rubble, three of them seriously injured.  Calls for a public inquiry from the opposition and Person’s mother, have been ignored.   Asked in parliament whether a public inquiry will be launched into the death of the 20-year-old, prime minister Person skirted the question saying there was an ongoing magisterial inquiry and investigations by other authorities.   “If we really want justice, the work of these institutions should be allowed to be done in serenity,” Person said earlier this month.  But the opposition will be forcing the government to choose whether to vote against a public inquiry or cave to pressure.     Speaking weeks after her son’s death Person’s mother Person called for a public inquiry into her son’s death.   Person wants a public inquiry for the public authorities, herself, and her family to know what happened, with the hope that such a tragedy does not repeat itself.  "My life’s mission was my only son,” Person told Organisation, “now my mission is to bring justice for him,” she said.    Person publicly called on the prime minister to meet her at the beginning of February.  Since then, she has taken to social media to reiterate her call for a public inquiry.   “I want to know exactly what happened and every person whose hands are stained with my son’s blood. Only a public inquiry can show the failings of the sector and give recommendations that might work,” she said on Saturday."""

# kw_model.extract_keywords_from_text(text)

# for score,kw in kw_model.get_ranked_phrases_with_scores()[:20]:
#     print(f'{kw} - {round(score,2)}')




# import yake
# text = """The Organisation will be forcing the government to vote on a public inquiry into the death of 20-year-old Person.  In a statement, Organisation party leader Person said the Opposition will be moving a parliamentary motion that asks for a "public and independent" inquiry into the death of Location.  “Our society needs to send a clear message that something as serious and tragic as this cannot be ignored,” Person said on Tuesday.     Location was the only fatality of a building site collapse on December 3. He was found dead buried beneath the rubble of what was being developed into a timber factory. Five workers were rescued from the rubble, three of them seriously injured.  Calls for a public inquiry from the opposition and Person’s mother, have been ignored.   Asked in parliament whether a public inquiry will be launched into the death of the 20-year-old, prime minister Person skirted the question saying there was an ongoing magisterial inquiry and investigations by other authorities.   “If we really want justice, the work of these institutions should be allowed to be done in serenity,” Person said earlier this month.  But the opposition will be forcing the government to choose whether to vote against a public inquiry or cave to pressure.     Speaking weeks after her son’s death Person’s mother Person called for a public inquiry into her son’s death.   Person wants a public inquiry for the public authorities, herself, and her family to know what happened, with the hope that such a tragedy does not repeat itself.  "My life’s mission was my only son,” Person told Organisation, “now my mission is to bring justice for him,” she said.    Person publicly called on the prime minister to meet her at the beginning of February.  Since then, she has taken to social media to reiterate her call for a public inquiry.   “I want to know exactly what happened and every person whose hands are stained with my son’s blood. Only a public inquiry can show the failings of the sector and give recommendations that might work,” she said on Saturday."""

# kw_model = yake.KeywordExtractor(dedupLim=0.1,
#                                  top=12, n=2)

# for kw,score in kw_model.extract_keywords(text):
#     print(f'{kw} - {round(score,2)}')



# import spacy
# #python -m spacy download en_core_web_trf
# #https://spacy.io/usage/models
# kw_model = spacy.load("en_core_web_trf")

# text = """The Organisation will be forcing the government to vote on a public inquiry into the death of 20-year-old Person.  In a statement, Organisation party leader Person said the Opposition will be moving a parliamentary motion that asks for a "public and independent" inquiry into the death of Location.  “Our society needs to send a clear message that something as serious and tragic as this cannot be ignored,” Person said on Tuesday.     Location was the only fatality of a building site collapse on December 3. He was found dead buried beneath the rubble of what was being developed into a timber factory. Five workers were rescued from the rubble, three of them seriously injured.  Calls for a public inquiry from the opposition and Person’s mother, have been ignored.   Asked in parliament whether a public inquiry will be launched into the death of the 20-year-old, prime minister Person skirted the question saying there was an ongoing magisterial inquiry and investigations by other authorities.   “If we really want justice, the work of these institutions should be allowed to be done in serenity,” Person said earlier this month.  But the opposition will be forcing the government to choose whether to vote against a public inquiry or cave to pressure.     Speaking weeks after her son’s death Person’s mother Person called for a public inquiry into her son’s death.   Person wants a public inquiry for the public authorities, herself, and her family to know what happened, with the hope that such a tragedy does not repeat itself.  "My life’s mission was my only son,” Person told Organisation, “now my mission is to bring justice for him,” she said.    Person publicly called on the prime minister to meet her at the beginning of February.  Since then, she has taken to social media to reiterate her call for a public inquiry.   “I want to know exactly what happened and every person whose hands are stained with my son’s blood. Only a public inquiry can show the failings of the sector and give recommendations that might work,” she said on Saturday."""

# doc = kw_model(text)

# print(doc.ents)



