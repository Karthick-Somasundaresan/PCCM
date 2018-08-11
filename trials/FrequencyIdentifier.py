import nltk

from nltk.corpus import wordnet

word = nltk.Text("Running")

fdist1=nltk.FreqDist(word)
fdist1.most_common(50)

