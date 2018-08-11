import nltk
from nltk.corpus import wordnet
from nltk.corpus import lin_thesaurus as cs

#syns = cs.scored_synonyms('pillage')
#print syns
#syn = cs.synonyms('pillage')
for entry in cs.scored_synonyms('pillage'):
    print entry[0]
    score = 0.0
    word = ""
    for words in entry[1]:
        #print words[0], words[1]
        if score < words[1]:
            score = words[1]
            word = words[0]
    print word, score
print cs.scored_synonyms('pillage')

#meaning = wordnet.synsets('pillage')[0].lemmas()[0].name()
#print wordnet.synsets('pillage')[0].lch_similarity(meaning, "n")
#print syns
#print dir(wordnet.synsets('pillage'))
#print meaning

#print wordnet.wup_similiarity(wordnet.synsets('pillage'), meaning)
#w1 = wordnet.synset('run.v.01')
#w2 = wordnet.synset('sprint.v.01')
#print w1.wup_similarity(w2)
