import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

#Documents
a = 'I am going to the toilet.'
b = 'Where are you going I must ask?'

vectorizer = TfidfVectorizer()

tfidf = vectorizer.fit_transform([a,b])
denselist = tfidf.todense().tolist()
feature_names = vectorizer.get_feature_names()

df = pd.DataFrame(denselist, columns=feature_names)
similarity = tfidf * tfidf.T
print(similarity)





