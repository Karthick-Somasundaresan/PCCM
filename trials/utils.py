import json
import os
import sqlite3
import math


aoa_db_loc = "/Users/karsomas/BITS/Project/data/sqlite_dbs/AoA.db"
freq_db_loc = "/Users/karsomas/BITS/Project/data/sqlite_dbs/WordFrequency.db"
# def get_median(sorted_arr):
#     print sorted_arr
#     num_entries = len(sorted_arr)
#     mid_val = num_entries / 2
#     if mid_val % 2 == 0:
#         median = sorted_arr[mid_val]
#     else:
#         median = (sorted_arr[mid_val] + sorted_arr[mid_val + 1]) / 2
#     return median

def get_db_conn(db_loc):
    conn = sqlite3.connect(db_loc)
    return conn

def get_median(sorted_arr):
    if len(sorted_arr) % 2 == 0:
        mid_val = (sorted_arr[int(len(sorted_arr) / 2)] + sorted_arr[int(len(sorted_arr) / 2) - 1]) / 2
    else:
        mid_val = sorted_arr[int(len(sorted_arr) / 2)]
    return mid_val


def sort_dic_on_value(dic, field="AoA"):
    key_list = []
    val_list = []
    for key, value in sorted(dic.items(), key=lambda x: x[1][field]):
        key_list.append(key)
        val_list.append(value[field])

    return key_list, val_list


def get_five_num_summary(score_doc, field):

    five_num_summ = {}
    min_val = q1 = median = q2 = max_val = 0
    # score_doc     - is a dic containing words {word: <AoA_Val>}
    # sorted_words  - after sorting based on AoA_Val key part of the score_doc
    # sorted_value  - after sorting based on AoA_Val value part of the score_doc
    # print(score_doc)
    if isinstance(score_doc, dict):
        sorted_words, sorted_value = sort_dic_on_value(score_doc, field)
        min_val = score_doc[sorted_words[0]][field]
        max_val = score_doc[sorted_words[-1]][field]
    elif isinstance(score_doc, list):
        score_doc.sort()
        min_val = score_doc[0]
        max_val = score_doc[-1]
        sorted_value = list(score_doc)
    median = get_median(sorted_value) # This is otherwise known as q2
    sub_list_low = list(sorted_value[0:int(len(sorted_value)/2) + 1])
    sub_list_low[-1] = median
    sub_list_high = list(sorted_value[int(len(sorted_value)/2):])
    sub_list_high[0] = median
    q1 = get_median(sub_list_low)
    q3 = get_median(sub_list_high)
    five_num_summ["min_val"] = min_val
    five_num_summ["max_val"] = max_val
    five_num_summ["median"] = median
    five_num_summ["q1"] = q1
    five_num_summ["q3"] = q3

    return five_num_summ


def load_mov_det(assetId):
    with open("data/"+ assetId + ".json", "r") as fp:
        mov_json = json.load(fp)
    return mov_json

#TODO - Have to get the actual subtitles location for the given assetId
def get_subtitles_for_asset(assetId):
    return "subtitles/original/Pirates_of_the_Caribbean_The_Curse_of_the_Black_Pearl.webvtt"

def get_word_scr(word_lst):
    aoa_conn = get_db_conn(aoa_db_loc)
    freq_conn = get_db_conn(freq_db_loc)
    aoa_cur = aoa_conn.cursor()
    freq_cur = freq_conn.cursor()
    formed_clause = ""
    for word in word_lst:
        if formed_clause == "":
            formed_clause = "\'" + word + "\'"
        else:
            formed_clause = formed_clause + ", \'" + word + "\'"
    
    aoa_formed_cmd = "".join("select Word, AoA_Kup_lem from AoA_words where Word in (") + formed_clause + ")"
    # print("Formed cmd:", aoa_formed_cmd)
    results = aoa_cur.execute(aoa_formed_cmd).fetchall()
    alt_scr = {}
    for row in results:
        alt_scr[row[0]] = {}
        try:
            value = float(row[1])
        except ValueError as VE:
            value = float(25)
        alt_scr[row[0]]["AoA"] = value
    freq_formed_cmd = "".join("select Word, Lg10WF from SUBTLEX_US where Word in (") + formed_clause + ")"
    # print("Formed Cmd:", freq_formed_cmd)
    results = freq_cur.execute(freq_formed_cmd).fetchall()
    for row in results:
        if row[0] not in alt_scr:
            alt_scr[row[0]]={}
            alt_scr[row[0]]["AoA"] = float(25)
        try:
            value = float(row[1])
        except ValueError as VE:
            value = float(0)
        alt_scr[row[0]]["Freq"] = value
    
    # print("alternate Scores:", alt_scr)
    return alt_scr


#word_det: {"Freq": 2.323, "AoA": 7.32}
#src_pt: (x, y) (AoA, Freq)
def get_dist_from_pt(word_det, src_pt):
    # med_scr (freq_val, aoa_val)
    if "Freq" not in word_det:
        word_det["Freq"] = 0
    if "AoA" not in word_det:
        word_det["AoA"] = 25
    dist = math.sqrt(math.pow((src_pt[1] - word_det["Freq"]), 2) + math.pow((src_pt[0] - word_det["AoA"]), 2))
    return dist

if __name__ == "__main__":
    get_word_scr(['parley', 'negotiation', 'dialogue', 'talks'])
