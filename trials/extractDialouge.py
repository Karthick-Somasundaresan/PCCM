import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def filter_words(words):
    stop_words = set(stopwords.words('english'))
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    filtered_words = [w for w in words if not w[0] in stop_words and not w[0] in punctuations]
    return filtered_words


def extract_dialogue(file_name):

    file_ptr = open(file_name, "r")
    for line in file_ptr:
        if line[0].isdigit() or line[0].isspace() or not line[0].isalpha():
            continue
        else:
            print(line,)
            words = word_tokenize(line)
            tagged = nltk.pos_tag(words)
            print(tagged)
            filtered_words = filter_words(tagged)
            print("----------------------------------------")
            words = line.split(" ")
            print("words", words)
            print("filtered words", filtered_words)
    print("fileName:", os.path.basename(file_name))
    mod_filename = "mod_" + os.path.basename(file_name)
    print("Modified FileName:", mod_filename)


extract_dialogue("/Users/karsomas/BITS/Project/Subtitles/Pirates_of_the_Caribbean_The_Curse_of_the_Black_Pearl.DVDRip.aXXo.en.srt")