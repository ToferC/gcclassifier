# Text pre-processing

# Import Gensim & NLTK

from gensim import corpora, models
from gensim.utils import simple_preprocess, lemmatize
from gensim.parsing.preprocessing import STOPWORDS as STOPWORDS

from nltk.tokenize import RegexpTokenizer
from nltk import word_tokenize

tokenizer = RegexpTokenizer(r'\w+')

from classifier.utility_scripts import load_obj

from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *

from nltk.corpus import stopwords
import nltk

from langdetect import detect_langs

import numpy as np

from classifier.rake import Rake

# Set up text processing

count_vectorizer = load_obj("count_vectorizer")
community_names = load_obj("community_names")

rake = Rake("SmartStoplist.txt",
    min_char_length=3, 
    max_words_length=5, 
    min_keyword_frequency=3)

# create French stop word list
fr_stops = set(stopwords.words('french'))

# Add certain additional stop words
public_service_stops = '''public service canada work http 
https travail gcconnex url'''.split()

# Set up stemmer
stemmer = SnowballStemmer("english")

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def tokenize(text):
    return [lemmatize_stemming(token) for token in tokenizer.tokenize(str(text))
            if token not in STOPWORDS if token not in fr_stops
           if token not in public_service_stops if len(token) > 3]

# Pre-processing

def pre_process(text):
	tokens = tokenize(text)
	tokens = " ".join(tokens)

	tokens_count = count_vectorizer.transform([tokens])
	return tokens_count


def find_language(text):

    language_list = list(detect_langs(text))

    language_text = "<p>"

    results_list = []
            
    for lang in language_list:
        l, p = str(lang).split(":")

        results_list.append(l)

        #language_text += f"{l.upper()}: {round(float(p),2)}"

    if results_list == ['en', 'fr'] or results_list == ['fr', 'en']:
        language_text = "Bilingual"
    elif results_list == ['fr']:
        language_text = "French"
    else:
        language_text = "English"

    language_text += ""

    return language_text


def find_keywords(text):

    keywords = rake.run(text)

    return_text = []

    for keyword in keywords[:4]:
        return_text.append(keyword[0]) #: score: {round(keyword[1],2)}</p>"

    return " ".join(return_text)


def predict_communities(predict_array):
    predict_dict = {}
    for i, element in enumerate(np.nditer(predict_array)):
        predict_dict[community_names[i]] = round(float(element),2)
    return predict_dict
