import json
import sqlite3
import trials.utils as utils
from nltk import word_tokenize


def get_best_within_usr_range(alt_info, usr_scr):
    bst_wrd = ""
    least_scr = 1000
    for word in alt_info:
        if alt_info[word]["AoA"] < usr_scr[0] and alt_info[word]["Freq"] > usr_scr[1] \
        or alt_info[word]["AoA"] <= float(usr_scr[0]/2):
            if alt_info[word]["AoA"] < least_scr:
                least_scr = alt_info[word]["AoA"]
                best_wrd = word
    return bst_wrd


def get_best_outside_usr_range(alt_info, usr_scr):
    bst_wrd = ""
    least_dist = 1000
    for word in alt_info:
        dist = utils.get_dist_from_pt(alt_info[word], usr_scr)
        if dist < least_dist:
            least_dist = dist
            bst_wrd = word
    return bst_wrd


def get_best_score(line_dict, line, usr_scr):
    line_of_interest = line_dict[line]
    # print("Line of Interest:", line)
    best_wrd = ""
    for word in line_of_interest["hard_words"]:
        if word not in line_of_interest["tagged_hard_word"] or len(line_of_interest["tagged_hard_word"][word]["alternates"]) == 0:
            line_of_interest["tagged_hard_word"][word]["best_alternate"] = word
            best_wrd = word
        else:
            alt_info = line_of_interest["tagged_hard_word"][word]["alternates_scr"]

            # filters the words within the users Q1
            # pick the one with the least AoA
            # If none gets filtered, select the one which has the least distance from user's score
            # print("Searching replacement for word:", word, " in alternates:", alt_info)
            best_wrd = get_best_within_usr_range(alt_info, usr_scr)
            if best_wrd == "":
                best_wrd = get_best_outside_usr_range(alt_info, usr_scr)
            if best_wrd == "":
                best_wrd = word
            line_of_interest["tagged_hard_word"][word]["best_alternate"] = best_wrd
        # print("Word:", word, " bst_alt:", best_wrd)

    return best_wrd


def reconstruct_line(line_dict):
    # print("Inside reconstruct_line:")
    # print(line_dict)
    for line in line_dict:
        line_builder = ""
        for word in word_tokenize(line):
            if word in line_dict[line]["hard_words"] and line_dict[line]["tagged_hard_word"][word]["best_alternate"] != word:
                line_builder = line_builder + " " +word
                line_builder = line_builder + " ( " + line_dict[line]["tagged_hard_word"][word]["best_alternate"] + " ) " 
            else:
                line_builder = line_builder + " " + word
        
        line_dict[line]["reconstructed_line"] = line_builder

    return


def select_best_alternative_for_lines(line_dict, usr_scr):

    for line in line_dict:
        if "tagged_hard_word" in line_dict[line]:
            for hard_word in line_dict[line]["tagged_hard_word"]:
                # for alternate in line_dict[line]["tagged_hard_word"][hard_word]["alternates"]:
                alternates = line_dict[line]["tagged_hard_word"][hard_word]["alternates"]
                # print("hard_word:", hard_word)
                if len(alternates) > 0:
                    alt_wrd_scr_det = utils.get_word_scr(alternates)
                    line_dict[line]["tagged_hard_word"][hard_word]["alternates_scr"] = alt_wrd_scr_det
                    #print("After construction:",line_dict[line])
        get_best_score(line_dict, line, usr_scr)



    return line_dict


if __name__ == "__main__":
    with open("data/line_full_det.json", "r") as fp:
        line_json = json.load(fp)
    
    line_dict = select_best_alternative_for_lines(line_json, (9.1, 3.3))
    reconstruct_line(line_dict)
    modified_fp = open("subtitles/modified/Personalized_captions.vtt", "w")
    with open("subtitles/original/Pirates_of_the_Caribbean_The_Curse_of_the_Black_Pearl.webvtt") as vtt:
        for line in vtt:
            if line in line_dict:
                modified_fp.write(line_dict[line]["reconstructed_line"])
            else:
                modified_fp.write(line)
    
    modified_fp.close()
        
    # for line in line_dict:
    #     print("Orig Line: ", line)
    #     print("Alter Line: ", line_dict[line]["reconstructed_line"])