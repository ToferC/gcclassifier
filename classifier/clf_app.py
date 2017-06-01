from flask import Flask
from flask import request
from flask import render_template

from langdetect import detect_langs, detect

from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC, SVC
from sklearn.preprocessing import MultiLabelBinarizer

import numpy as np

from utility_scripts import load_obj, save_obj
from text_preprocessing import lemmatize_stemming, tokenize

import rake

rake = rake.Rake("SmartStoplist.txt",
    min_char_length=3, 
    max_words_length=5, 
    min_keyword_frequency=3)

# Load models and data

count_vectorizer = load_obj("count_vectorizer")
multilabel_clf = load_obj("multilabel_clf")
community_names = load_obj("community_names")

# Flask app

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("text_input.html")

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']

    language = find_language(text)

    keywords = find_keywords(text)

    processed_text = pre_process(text)
    predicted_values = multilabel_clf.predict_proba(processed_text)
    predicted_output = predict_communities(predicted_values)
    return f'''<h3>Text</h3>
            <p>{text}</p>
            <h3>Language</h3>
            <p>{language}</p>
            <h3>Keywords</h3>
            <p>{keywords}</p>
            <h3>Audiences</h3>
            <p>{predicted_output}</p>'''

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

        language_text += f"<p>{l.upper()}: {round(float(p),2)}</p>"

    '''
    if results_list == ['en', 'fr'] or results_list == ['fr', 'en']:
        language_text += "EN/FR"
    elif results_list == ['fr']:
        language_text += "FR"
    else:
        language_text += "EN"'''

    language_text += "</p>"

    return language_text


def find_keywords(text):

    keywords = rake.run(text)

    return_text = ""

    for keyword in keywords[:4]:
        return_text += f"<p>{keyword[0]}: score: {round(keyword[1],2)}</p>"

    return return_text


def predict_communities(predict_array):
    predict_string = '''<table class='zebra'>
                        <tbody>
                        <th>Community</th><th>Prediction</th>'''
    for i, element in enumerate(np.nditer(predict_array)):
        predict_string += "<tr><td>{}</td>: <td>{}</td></tr>".format(community_names[i], round(float(element),2))
    predict_string += "</tbody></table>"
    return predict_string


if __name__ == '__main__':
    app.run()