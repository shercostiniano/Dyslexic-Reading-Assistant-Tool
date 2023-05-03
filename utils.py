import os
import string
import subprocess
from openpyxl import load_workbook
from nltk.corpus import stopwords

def sentence_to_list_without_stopwords(sentence):
    """
    Function for transforming a given text file into a list of list removing tl/en stopwords in the process.

    Args:
        filename (str): The file location of the text file.

    Returns:
        sentence_list: a list of strings containing sentences found on the file (without stopwords).
    """
    sentence_list = []
    tl_stop_words_list = get_stopwords_from_file('model/dictionary/tl_stopwords_modified.txt')
    en_stop_words_list = list(stopwords.words('english'))  # Uses nltk stopwords
    stopwords_list = tl_stop_words_list + en_stop_words_list
    words_list = sentence.split()
    filtered_sentence = [word for word in words_list if word not in stopwords_list]
    return filtered_sentence

def get_stopwords_from_file(filename):
    """
    Function for transforming stop words in a given file to a list. Can use read_text_file instead.

    Args:
        filename (str): The file location of the text file.

    Returns:
        stopwords_list: a list containing the stopwords found on the text file.
    """
    stopwords_list = []
    file = open(filename)
    for line in file:
        stopwords_list.append(line.rstrip())
    file.close()
    return stopwords_list

def process_data(str):
    input = str.split()
    text = ''
    ents = []

    for i, word in enumerate(input):
        text += f'{word}' if i == 0 else f' {word}'
        ents.append({
            'word': word,
            'start': 0 if i == 0 else len(text) - len(word),
            'end': len(text),
        })
    
    
    return {'text': text, 'ents': ents}
