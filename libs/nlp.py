import re
import numpy as np
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()

df_alay_dict = pd.read_csv('data/new_kamusalay.csv', encoding='latin-1', header=None)
df_alay_dict = df_alay_dict.rename(columns={0: 'original', 1: 'replacement'})

df_id_stopword_dict = pd.read_csv('data/stopwordbahasa.csv', header=None)
df_id_stopword_dict = df_id_stopword_dict.rename(columns={0: 'stopword'})

def lowercase(text):
    return text.lower()

def remove_unnecessary_char(text):
    text = re.sub('\n',' ',text) # Remove every '\n'
    text = re.sub('rt',' ',text) # Remove every retweet symbol
    text = re.sub('user',' ',text) # Remove every username
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) # Remove every URL
    text = re.sub('  +', ' ', text) # Remove extra spaces
    return text
    
def remove_nonaplhanumeric(text):
    text = re.sub('[^0-9a-zA-Z]+', ' ', text) 
    return text

alay_dict_map = dict(zip(df_alay_dict['original'], df_alay_dict['replacement']))
def normalize_alay(text):
    return ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])

def remove_stopword(text):
    text = ' '.join(['' if word in df_id_stopword_dict.stopword.values else word for word in text.split(' ')])
    text = re.sub('  +', ' ', text) # Remove extra spaces
    text = text.strip()
    return text

def stemming(text):
    return stemmer.stem(text)

def preprocess_tweets(text):
    text = lowercase(text) 
    text = remove_nonaplhanumeric(text) 
    text = remove_unnecessary_char(text) 
    text = normalize_alay(text) 
    text = stemming(text) 
    text = remove_stopword(text)
    return text
 
def preprocess_file(file):
    file['Tweet'] = file['Tweet'].apply(preprocess_tweets)
    return file