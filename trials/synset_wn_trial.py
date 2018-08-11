import nltk
from nltk.corpus import wordnet

meaning = wordnet.synsets('pillage')[0].lemmas()[0].name()
print meaning
print wordnet.synset('pillage.n.01')
for sets in wordnet.synsets('pillage'):
    print sets
    print sets.definition()
    print "WUP score:", wordnet.synset('pillage.n.01').wup_similarity(sets)
    #print "LCH score:", wordnet.synset('pillage.n.01').lch_similarity(sets)
    print "PATH score:", wordnet.synset('pillage.n.01').path_similarity(sets)

print "############################"

#print dir(wordnet.synsets('pillage')[0])
print wordnet.synsets('pillage')[0].pos()
for sets in wordnet.synsets('pillage'):
    print wordnet.synset('pillage.v.01').wup_similarity(sets)
w1 = wordnet.synset('run.v.01')
w2 = wordnet.synset('sprint.v.01')
print w1.wup_similarity(w2)

