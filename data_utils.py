###################################################################################
#
# THESIS TITLE: EXTRACTING AND ORGANIZING DISASTER-RELATED PHILIPPINE COMMUNITY
#               RESPONSES FOR AIDING NATIONWIDE RISK REDUCTION PLANNING AND
#               RESPONSE (2020)
#
# AUTHOR/DEVELOPER: Nicco Nocon
# INSTITUTION: De La Salle University, Manila
# EMAIL: noconoccin@gmail.com or nicco_louis_nocon@dlsu.edu.ph
# CONTACT NUMBER: (+63) 917 819 9311
#
# SOURCE OF FUNDING: Philippine-California Advanced Research Institutes (PCARI)
#                    through Commission on Higher Education and Department of
#                    Science and Technology – Science Education Institute
#
###################################################################################
# DATA UTILITIES
# Used for processing Malasakit Responses excel file and text file resources
# > Malasakit: https://opinion.berkeley.edu/pcari/en/landing/
# > Paper: https://ieeexplore.ieee.org/document/8239265
###################################################################################

from openpyxl import load_workbook
from nltk.corpus import stopwords
import string

def text_to_list(filename):
    """
    Function for transforming a given text file into a list of list [s1[w1,w2,...,wN], ..., sN[w1,w2,...,wN]].

    Args:
        filename (str): The file location of the text file.

    Returns:
        sentence_list: a list of strings containing sentences found on the file.
    """
    sentence_list = []
    file = open(filename)
    for line in file:
        sentence_list.append(line.split())  # Returns a white-spaced split list of words and store in sentence_list
    file.close()
    return sentence_list


def text_to_list_without_stopwords(filename):
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
    file = open(filename,encoding='utf-8')
    for line in file:
        line = str(line).lower()
        words_list = line.split()
        filtered_sentence = [word for word in words_list if word not in stopwords_list]
        sentence_list.append(filtered_sentence)  # Returns a white-spaced split list of words and store in sentence_list
    file.close()
    return sentence_list

def sentence_to_list_without_stopwords(sentence, path='tl_stopwords_modified.txt'):
    """
    Function for transforming a given text file into a list of list removing tl/en stopwords in the process.

    Args:
        filename (str): The file location of the text file.

    Returns:
        sentence_list: a list of strings containing sentences found on the file (without stopwords).
    """
    tl_stop_words_list = get_stopwords_from_file(path)
    en_stop_words_list = list(stopwords.words('english'))  # Uses nltk stopwords
    stopwords_list = tl_stop_words_list + en_stop_words_list
    words_list = sentence.split()
    filtered_sentence = [word for word in words_list if word not in stopwords_list]
    return filtered_sentence

def write_text_file(filename, string_list):
    """
    Function that writes the strings in a list to a text file. Normally to be read by the normalizer module.

    Args:
        filename (str): The file location of the text file.
        string_list: The list to be written in the text file.
    """
    file = open(filename, 'w+',encoding='utf-8')
    for element in string_list:
        if isinstance(element,list):
            file.write(' '.join(element) + '\n')
        elif isinstance(element,str):
            file.write(element + '\n')  # Write per element/line in the list
    file.close()


def read_text_file(filename):
    """
    Function that reads the strings in a file and transfer them into a list.

    Args:
        filename (str): The file location of the text file.

    Returns:
        string_list: a list containing the contents of the text file.
    """
    file = open(filename, 'r', encoding='utf-8')
    string_list = file.readlines()  # Put in the list the string contents per new line
    string_list = list(map(lambda sentence: sentence.strip(), string_list))  # Remove \n
    file.close()
    return string_list


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
