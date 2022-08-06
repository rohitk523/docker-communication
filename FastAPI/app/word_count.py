from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import re
from collections import Counter
import pandas as pd

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

def txt_len(filename):
    string = open(filename,encoding='utf-8').read()
    count = 0
    for word in string.split():
        count+= len(word)
    return count

def list_keywords(filename):
    string = pd.read_csv(filename)
    return str(list(string.Keywords))

def keywords_word_count(txtfile, csvfile):
    string = pd.read_csv(csvfile)
    names=dict(word_count(txtfile))
    given_list = list(string.Keywords)
    filtered_dict = dict(filter(lambda item: item[0] in given_list , names.items()))
    if filtered_dict == {}:
        return "Word count for uploaded keywords was not found"
    else:
        return filtered_dict

def word_count(filename):
    string = open(filename,encoding='utf-8').read()
    op_string = re.sub(r'[^\w\s]','',string)
    tokenized_words = word_tokenize(op_string)
    stops = stopwords.words('english')
    words = [word for word in tokenized_words if word not in stops]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    my_count = Counter(words)
    return my_count