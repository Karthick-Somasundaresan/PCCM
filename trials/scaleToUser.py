import json
import trials.utils as utils
import trials.MovieAnalyser as MovieAnalyser
import trials.UserScore as UserScore
from random import randint
from nltk.corpus import wordnet
from nltk import word_tokenize

def get_alternates(assetId, word_dic, usr_scr):
    hard_word_lst = []
    for word in word_dic:
        if word_dic[word]["AoA"] > usr_scr[0] and word_dic[word]["Freq"] < usr_scr[1]:
            hard_word_lst.append(word)
    track_filename = utils.get_subtitles_for_asset(assetId)

    print("Hardwords list:", len(hard_word_lst))
    print("Hardwords list:", hard_word_lst)
    with open(track_filename, "r") as track_fd:
        for line in track_fd:
            if any(word in line for word in hard_word_lst):
                print(line)




    return hard_word_lst



if __name__ == "__main__":
    mov_json = utils.load_mov_det("asset1")
    # samples = MovieAnalyser.get_samples_for_movie("asset1")
    # sam_copy = list(samples)
    # no_of_samples = randint(0, len(samples) - 1)
    # usr_resp = []
    # print("Number of User Response:", no_of_samples)
    # for count in range(0, no_of_samples):
    #     index = randint(0, len(sam_copy) - 1)
    #     usr_resp.append(sam_copy[index])
    #     del sam_copy[index]
    # print("User Response:", usr_resp)
    # format (aoa_scr, freq_scr)
    #usr_resp = ['ideas', 'pair', 'ambushing', 'hob', 'bootstraps', 'mutineers', 'gallivanting', 'buccaneer', 'extort', 'plunder', 'wreaked', 'savvy', 'dauntless', 'betrayers', 'meaning', 'trick', 'feckless']
    usr_resp = [ 'trick', 'stole', 'ideas', 'pair', 'meaning', 'betrayers', 'wreaked', 'savvy']
    usr_scr = UserScore.analyze_usr_scr("asset1", usr_resp)
    get_alternates("asset1", mov_json["asset1"]["det_mov_scr"], usr_scr)
    print("User Score:", usr_scr)

