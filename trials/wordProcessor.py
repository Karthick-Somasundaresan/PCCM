from nltk.corpus import wordnet, brown
from nltk import word_tokenize
from nltk import DefaultTagger
from nltk import UnigramTagger
from nltk import BigramTagger
from nltk.tag.stanford import StanfordPOSTagger
import json
import trials.lineSynth as lineSynth


nltk_pos_map = {"v": ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "VERB"],
           "n": ["NN", "NNS", "NNP", "NNPS", "NOUN"],
           "a": ["JJ", "JJR", "JJS", "ADJ"],
           "r": ["RB", "RBR", "RBS", "ADV"]}

def get_mapped_pos(pos):
    for key in nltk_pos_map:
            if pos in nltk_pos_map[key]:
                return key

def get_tagger(type="StandfordPOSTagger"):
    if type == "Custom":
        brown_tagged_sents = brown.tagged_sents(categories='news', tagset='universal')
        t0 = DefaultTagger('NOUN')
        t1 = UnigramTagger(brown_tagged_sents, backoff=t0)
        t2 = BigramTagger(brown_tagged_sents, backoff=t1)
    else:
        t2 = StanfordPOSTagger('data/./models/wsj-0-18-bidirectional-distsim.tagger', '3rdparty_libs/stanford-postagger.jar')

    return t2


def mark_pos_for_line(line, tagger):
    tagged_words = []
    tagged_words = tagger.tag(word_tokenize(line))
    return tagged_words


def get_hard_words_in_line(line, hard_word_lst):
    all_words = word_tokenize(line)
    interested_words = []
    for word in all_words:
        if word in hard_word_lst:
            interested_words.append(word)
    return interested_words


def substitute_lines(lines_of_interest, hard_word_lst, usr_scr, tagged_lines):
    line_mapper = {}
    tagger =get_tagger()
    print("Identifying PoS for lines using StandfordPOSTagger...")
    for line in lines_of_interest:
        words_to_replace = get_hard_words_in_line(line, hard_word_lst)
        # print("Line:", line.strip(), "hard_words:", words_to_replace)
        if tagged_lines is None:
            tagged_words = mark_pos_for_line(line, tagger)
        else:
            tagged_words = tagged_lines[line.strip()]
        # print("Tagged Words:", tagged_words)
        line_mapper[line] ={ "tagged_line": tagged_words, "hard_words": words_to_replace}

    print("Identifying PoS for hard-words...")
    get_pos_for_hard_words(line_mapper)
    print("Looking Wordnet for alternative words")
    get_all_meanings_for_hard_words(line_mapper)
    print("Selecting the best alternative")
    line_dict = lineSynth.select_best_alternative_for_lines(line_mapper, (9.1, 3.3))
    print("Reconstructing in lines with alternates")
    lineSynth.reconstruct_line(line_dict)
    # with open("data/line_det.json", "w") as fp:
    #     json.dump(line_mapper, fp)
    return line_dict
    

def get_pos_for_hard_words(line_data):
    for line in line_data:
        for hard_word in line_data[line]["hard_words"]:
            for tag_tup in line_data[line]["tagged_line"]:
                print("Tagged_tup:", tag_tup, "hard_word:", hard_word)
                if "tagged_hard_word" not in line_data[line]:
                    line_data[line]["tagged_hard_word"] = {}
                if tag_tup[0] == hard_word:
                    line_data[line]["tagged_hard_word"][hard_word] = {"tag": tag_tup[1]}
                    break
            print("------------------------------------------------")
    print(line_data)
    return


def get_all_meanings_for_hard_words(line_data):
    for line in line_data:
        print(line)
        print(line_data[line])
        for hard_word in line_data[line]["hard_words"]:
            tag = line_data[line]["tagged_hard_word"][hard_word]["tag"]
            tag = get_mapped_pos(tag)
            # print("hard word:", hard_word, " tag:", tag)
            alt_words = list( map(lambda syn: syn.lemma_names(), wordnet.synsets(hard_word, tag)))
            full_alt = [w for packs in alt_words for w in packs]
            syn_hypernyms_lst = []
            syn_similartos_lst = []
            for syns in wordnet.synsets(hard_word, tag):
                syn_hypernyms_lst.append(syns.hypernyms())
                syn_similartos_lst.append(syns.similar_tos())
            hyper_lst = []
            for syn_lst in syn_hypernyms_lst:
                for syn in syn_lst:
                    hyper_lst = hyper_lst + syn.lemma_names()
            similar_lst = []
            for syn_lst in syn_similartos_lst:
                for syn in syn_lst:
                    similar_lst = similar_lst + syn.lemma_names()
            full_alt = full_alt + hyper_lst + similar_lst
            # print("Complete alt:", full_alt)
            line_data[line]["tagged_hard_word"][hard_word]["alternates"] = full_alt



if __name__ == "__main__":
    line_dat = {}
    with open("data/line_det.json", "r") as fp:
        line_dat = json.load(fp)
    # for keys in line_dat:
    #     print("--------------------------")
    #     print("Line: ", keys)
    #     print("Tagged Line: ", line_dat[keys]["tagged_line"])
    #     print("hard words in line: ", line_dat[keys]["hard_words"])
    get_pos_for_hard_words(line_dat)
    get_all_meanings_for_hard_words(line_dat)
    print(line_dat)

    with open("data/line_full_det.json", "w") as fp:
        json.dump(line_dat, fp)

