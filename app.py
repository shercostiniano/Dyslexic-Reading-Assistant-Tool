import os
import string
import json
import subprocess
import random
import pandas as pd
from flask_cors import CORS
from transformers import pipeline
from nltk import StanfordPOSTagger
from data_utils import sentence_to_list_without_stopwords
from flask import Flask, render_template, request, url_for, send_from_directory, redirect

from utils import process_data

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

java_path = "C:/Program Files/Java/jdk-19/bin/java.exe"
os.environ['JAVAHOME'] = java_path
ner_pipe = pipeline(model='scostiniano/istorya-roberta-filipino')
tagger = StanfordPOSTagger(
    'model/filipino-left5words-owlqn2-distsim-pref6-inf2.tagger', "model/stanford-postagger.jar")


class Book:
    def __init__(self, title, image, link):
        self.title = title
        self.image = image
        self.link = link

@app.before_request
def redirect_to_https():
    if request.headers.get('X-Forwarded-Proto') == 'http':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
    
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('images/favicon.ico'), 204

@app.route('/Mga-Ibon/')
def book1():
    return render_template('Mga-Ibon/index.html')


@app.route('/Si-Tata-at-si-Toto/')
def book2():
    return render_template('Si-Tata-at-si-Toto/index.html')


@app.route('/Takbo-Takbo-Takbo/')
def book3():
    return render_template('Takbo-Takbo-Takbo/index.html')


@app.route('/<path:path>')
def send_static(path):
    if path.endswith('/'):
        path += 'index.html'
    return send_from_directory('static', path)


@app.route('/')
def home():
    # Create a list of books
    books = [
        Book('Mga Ibon', 'Mga-Ibon/cover.jpg', 'Mga-Ibon/'),
        # Book('Si Tata at si Toto', 'Si-Tata-at-si-Toto/cover.jpg',
        #      'Si-Tata-at-si-Toto/'),
        # Book('Takbo Takbo Takbo', 'Takbo-Takbo-Takbo/cover.jpg',
        #      'Takbo-Takbo-Takbo/'),
    ]
    # Render the home template with the list of books
    return render_template('index.html', books=books)


@app.route('/<prefix>/<path:subpath>')
def modes(prefix, subpath):
    if subpath == 'review':
        return review(prefix)
    elif subpath == 'evaluate':
        return quiz(prefix)


def review(title):
    json_path = os.path.join(app.static_folder, f'{title}/words.json')
    with open(json_path, 'r') as f:
        data = json.load(f)
    words = data['review_words']

    for word in words:
        words[word]['image_url'] = url_for(
            'static', filename=f'images/{words[word]["image"]}')
        words[word]['audio_url'] = url_for(
            'static', filename=f'audios/{words[word]["audio"]}')

    return render_template('review.html', title=title, my_data=words)


def quiz(title):
    # Define the list of words for the quiz
    json_path = os.path.join(app.static_folder, f'{title}/words.json')
    with open(json_path, 'r') as f:
        data = json.load(f)
    words = data['quiz_words']
    return render_template('evaluate.html', word_list=words)

@app.route('/api/predict', methods=['POST'])
def predict():
    req = request.get_json()
    input = req['input']
    isNER = req['isNER']
    isPOS = req['isPOS']
    isSimplify = req['isSimplify']
    input = input.translate(str.maketrans('', '', string.punctuation)).lower()
    print(isNER, isPOS, isSimplify)
    if isSimplify:
        input = ' '.join(sentence_to_list_without_stopwords(
            input, path='model/dictionary/tl_stopwords.txt'))
        p1 = subprocess.run(['java', '-jar', '--enable-preview',
                             'model/com.stemmer.app.jar', input], capture_output=True, text=True)
        input = p1.stdout.split('\n')[-2:-1][0]

    if isNER or isPOS:
        try:
            pos = predict_pos(input) if isPOS else None
            ner = predict_ner(input) if isNER else None
            df = pd.merge(pos, ner, on=[
                'start', 'end', 'word'], how='left') if isPOS and isNER else pos if isPOS else ner
            df_json = df.to_json(orient="records")
            result = {"status": 1, "text": input, "ents": json.loads(df_json)}
        except Exception as e:
            print(e)
            result = {"status": 0,
                      "text": "Failed to analyze the text", "ents": []}
    else:
        result = {"status": 2, "text": input, "ents": []}
    return result


def predict_pos(input):
    pos_predict = tagger.tag(input.split())
    pos_list = ['-'.join(pos).split("|")[-1] for pos in pos_predict]
    data = process_data(input)
    df = pd.DataFrame(data['ents'])
    df['pos'] = pos_list
    df = df[df['pos'].str.contains("NN|VB|JJ")]

    return df


def predict_ner(input):
    ner_predict = ner_pipe(input)
    print(ner_predict)
    df = pd.DataFrame(ner_predict)
    df['word'] = df['word'].apply(lambda x: x.replace('Ġ', ''))
    df = df[df['score'] >= 0.75]
    return df


if __name__ == '__main__':
    app.run(debug=True, port=8080)
