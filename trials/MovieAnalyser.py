import json
import trials.utils as utils
import trials.sampler as sampler
from nltk.tokenize import word_tokenize
import trials.drawGraph as drawGraph

import os
import sqlite3

aoa_db_loc = "/Users/karsomas/BITS/Project/data/sqlite_dbs/AoA.db"
freq_db_loc = "/Users/karsomas/BITS/Project/data/sqlite_dbs/WordFrequency.db"


def get_db_conn(db_loc):
    #aoa_conn = sqlite3.connect("/Users/karsomas/BITS/Project/data/sqlite_dbs/AoA.db", check_same_thread=False)
    #freq_conn = sqlite3.connect("/Users/karsomas/BITS/Project/data/sqlite_dbs/WordFrequency.db", check_same_thread=False)
    conn = sqlite3.connect(db_loc)
    return conn


#aoa_cursor = aoa_conn.cursor()
#freq_cursor = freq_conn.cursor()


def filter_line(line):
    if line[0].isdigit() or line[0].isspace():
        return True
    else:
        return False


def get_movie_dialogues(filename):
    dialogues = ""
    text_track_file = open(filename, "r")
    for line in text_track_file:
        if filter_line(line):
            continue
        else:
            dialogues = dialogues + line

    return dialogues


def get_aoa_score(dialogues):
    tot_score = 0
    score = 0
    #print dialogues
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    word_cnt = 0
    word_dic = {}
    conn = get_db_conn(aoa_db_loc)
    cmd = "select Word, AoA_Kup_lem, Lemma_highest_PoS from AoA_words where Word="
    for word in word_tokenize(dialogues):
        if word in punctuations:
            continue
        formed_cmd = cmd + "\"" + word.lower() + "\""
        result = conn.cursor().execute(formed_cmd).fetchone()
        if result is None:
            #word_dic[word] = 25
            continue
        if result == "NA": # these words are not rated in AoA excel file itself. So giving maximum value.
            score = 25
        else:
            score = float(result[1])
            lemma = result[2]

        word_dic[result[0]] = {"AoA": score, "lemma": lemma}
        tot_score += score
        word_cnt += 1
    conn.close()
    return tot_score/word_cnt, word_dic




def get_freq_score(detail_aoa):
    avg_score = 0
    detail_score = detail_aoa
    formed_cmd = "select Lg10WF from SUBTLEX_US where Word="
    formed_clause = ""
    for word in detail_aoa:
        if formed_clause == "":
            formed_clause = "\'" + word + "\'"
        else:
            formed_clause = formed_clause + ",\'" + word + "\'"

    formed_cmd = "".join("select Word, Lg10WF from SUBTLEX_US where Word in (")
    formed_cmd = formed_cmd + formed_clause
    formed_cmd = formed_cmd + ")"
    tot_words = 0
    tot_freq = 0
    conn = get_db_conn(freq_db_loc)
    results = conn.cursor().execute(formed_cmd).fetchall()
    for rows in results:
        detail_score[rows[0]]["Freq"] = float(rows[1])
        tot_words += 1
        tot_freq += float(rows[1])

    avg_score = tot_freq / tot_words
    conn.close()

    return avg_score, detail_score


def get_movie_score(filename):
    dialogues = get_movie_dialogues(filename)
    avg_aoa_score, detail_aoa_score = get_aoa_score(dialogues)
    print("Avg Score:", avg_aoa_score)
    aoa_five_num_summ = utils.get_five_num_summary(detail_aoa_score, "AoA")
    print(aoa_five_num_summ)
    iqr = aoa_five_num_summ["q3"] - aoa_five_num_summ["q1"]
    aoa_outlier_boundary = 1.5 * iqr + aoa_five_num_summ["median"]
    print("Avg AoA Score:", avg_aoa_score, " AoA outlier boundary:", aoa_outlier_boundary)
    # for word in detail_aoa_score:
    #     if detail_aoa_score[word]['AoA'] > aoa_outlier_boundary:
    #         print word, detail_aoa_score[word]
    avg_freq_score, detailed_score = get_freq_score(detail_aoa_score)
    #print "Avg freq score", avg_freq_score, " detailed dict:", detailed_score
    freq_five_num_summ = utils.get_five_num_summary(detail_aoa_score, "Freq")
    print(freq_five_num_summ)
    iqr = freq_five_num_summ["q3"] - freq_five_num_summ["q1"]
    freq_outlier_boundary = freq_five_num_summ["median"] - 1.5 * iqr
    print("Average freq boundary:", avg_freq_score, " Freq outlier boundary:", freq_outlier_boundary)
    q1_cnt = q2_cnt = q3_cnt = q4_cnt = 0
    q1_lst = []
    q2_lst = []
    q3_lst = []
    q4_lst = []
    for word in detailed_score:
        #if detailed_score[word]['Freq'] < freq_outlier_boundary:
            #print word, detailed_score[word]
        if detailed_score[word]['Freq'] < freq_outlier_boundary and \
                detailed_score[word]['AoA'] > aoa_outlier_boundary:
            detailed_score[word]['Quad'] = "q4"
            q4_cnt += 1
            q4_lst.append(word)
        elif detailed_score[word]['Freq'] > freq_outlier_boundary and \
                detailed_score[word]['AoA'] > aoa_outlier_boundary:
            detailed_score[word]['Quad'] = "q3"
            q3_cnt += 1
            q3_lst.append(word)
        elif detailed_score[word]['Freq'] < freq_outlier_boundary and \
                detailed_score[word]['AoA'] < aoa_outlier_boundary:
            detailed_score[word]['Quad'] = "q2"
            q2_cnt += 1
            q2_lst.append(word)
        elif detailed_score[word]['Freq'] > freq_outlier_boundary and \
                detailed_score[word]['AoA'] < aoa_outlier_boundary:
            detailed_score[word]['Quad'] = "q1"
            q1_cnt += 1
            q1_lst.append(word)

    print("Number of words in q1:", q1_cnt, " q2:", q2_cnt, " q3:", q3_cnt, " q4:", q4_cnt, " len:", len(detailed_score))
    print("Ratio of q1:", q1_cnt/len(detailed_score), " q2:", q2_cnt/len(detailed_score), " q3:", \
        q3_cnt/len(detailed_score), " q4:", q4_cnt/len(detailed_score))

    return detailed_score, aoa_outlier_boundary, freq_outlier_boundary


def get_samples(detailed_mov_scr):
    # frq_wrd_lst, frq_scr_lst = utils.sort_dic_on_value(detailed_mov_scr, "Freq")
    # aoa_wrd_lst, aoa_scr_lst = utils.sort_dic_on_value(detailed_mov_scr, "AoA")
    # sel_frq_idx = sampler.pop_sampler(frq_scr_lst, 10)
    # sel_aoa_idx = sampler.pop_sampler(aoa_scr_lst, 10)
    # print "Selected words for freq scaling", sel_frq_idx
    # for idx in sel_frq_idx[1]:
    #     print frq_wrd_lst[idx], det_mov_scr[frq_wrd_lst[idx]]['Quad']
    # print "Selected words for aoa scaling", sel_aoa_idx
    # for idx in sel_aoa_idx[1]:
    #     print aoa_wrd_lst[idx], det_mov_scr[aoa_wrd_lst[idx]]['Quad']
    #
    sample_lst = sampler.four_cluster_sampling(detailed_mov_scr, 5)
    print(sample_lst)
    return sample_lst



    #avg_freq_score, detail_freq_score = get_freq_score()
def get_samples_for_movie(movie_id):
    det_mov_scr, aoa_out, freq_out = get_movie_score("/Users/karsomas/BITS/Project/Subtitles/Pirates_of_the_Caribbean_The_Curse_of_the_Black_Pearl.DVDRip.aXXo.en.srt")
    mov_sam, q1_avg, q2_avg, q3_avg, q4_avg = get_samples(det_mov_scr)
    mov_dic = {movie_id: {"det_mov_scr": det_mov_scr}, "q1_avg": q1_avg, "q2_avg": q2_avg, "q3_avg": q3_avg, "q4_avg": q4_avg, "aoa_out": aoa_out, "freq_out": freq_out}
    mov_json = json.dumps(mov_dic)
    fd = open("data/" + movie_id + ".json", "w")
    fd.write(mov_json)
    fd.close()
    return mov_sam


if __name__ == "__main__":
    get_samples_for_movie("someId")




