from nltk.corpus import wordnet


#print dir(wordnet.synsets('pillage')[0])
#print dir(wordnet)
# for sets in wordnet.synsets('pillage'):
#     #print sets.definition()
#     print sets.lemma_names()
#     print "hypernyms", sets.hypernyms() #this returns a synset
#     print "hyponyms", sets.hyponyms() #this returns a synset
    #for hset in sets.hypernyms():
        #print hset.lemma_names()
    #print sets.lemmas()[0].name(), sets.lemmas()[0].count()
# w1 = wordnet.synset('run.v.01')
# w2 = wordnet.synset('sprint.v.01')
# print w1.wup_similarity(w2)

print "##################"
subList = []
for ss in wordnet.synsets('brigandage', pos="v"):
    subList = subList + ss.lemma_names()
    for simWords in ss.similar_tos():
        subList = subList + simWords.lemma_names()

print "Alternates:", subList
for wds in subList:
    print wds
