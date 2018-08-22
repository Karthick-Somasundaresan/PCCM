import json
import trials.utils as utils
import trials.MovieAnalyser as MovieAnalyser
import trials.UserScore as UserScore
import trials.wordProcessor as word_processor
from random import randint
import os.path

# def get_alternates(assetId, word_dic, usr_scr):
def get_alternates(assetId, usr_scr):
    hard_word_lst = []
    word_dic = {}
    print("Finding HardwordList:\n")
    with open("data/" + assetId + ".json") as fp:
        mov_json = json.load(fp)
    word_dic = mov_json[assetId]["det_mov_scr"]
    # print(word_dic)
    for word in word_dic:
        if word_dic[word]["AoA"] > usr_scr[0] and word_dic[word]["Freq"] < usr_scr[1]:
            hard_word_lst.append(word)
    track_filename = utils.get_subtitles_for_asset(assetId)

    print("Total Hardwords in Movie:", len(hard_word_lst))
    lines_of_interest = []
    with open(track_filename, "r") as track_fd:
        for line in track_fd:
            if any(word in line for word in hard_word_lst):
                lines_of_interest.append(line)
    
    tagged_lines = None
    try:
        asset_tagged_file = "data/" + assetId+ "_tagged_lines.json"
        with open(asset_tagged_file, "r") as fp:
            tagged_lines = json.load(fp)
    except FileNotFoundError as exception:
        print("File Not found:", asset_tagged_file)
    print("Found lines containing hard words")
    line_details = word_processor.substitute_lines(lines_of_interest, hard_word_lst, usr_scr, tagged_lines=tagged_lines)
    print("Inserting alternates in the dialogue")
    utils.generate_new_dialogues(assetId, line_details)

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

