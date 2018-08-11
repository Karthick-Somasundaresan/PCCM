
# def get_median(sorted_arr):
#     print sorted_arr
#     num_entries = len(sorted_arr)
#     mid_val = num_entries / 2
#     if mid_val % 2 == 0:
#         median = sorted_arr[mid_val]
#     else:
#         median = (sorted_arr[mid_val] + sorted_arr[mid_val + 1]) / 2
#     return median


def get_median(sorted_arr):
    if len(sorted_arr) % 2 == 0:
        mid_val = (sorted_arr[int(len(sorted_arr) / 2)] + sorted_arr[int(len(sorted_arr) / 2) - 1]) / 2
    else:
        mid_val = sorted_arr[int(len(sorted_arr) / 2)]
    return mid_val


def sort_dic_on_value(dic, field="AoA"):
    key_list = []
    val_list = []
    for key, value in sorted(dic.iteritems(), key=lambda x: x[1][field]):
        key_list.append(key)
        val_list.append(value[field])

    return key_list, val_list


def get_five_num_summary(score_doc, field):

    five_num_summ = {}
    min_val = q1 = median = q2 = max_val = 0
    # score_doc     - is a dic containing words {word: <AoA_Val>}
    # sorted_words  - after sorting based on AoA_Val key part of the score_doc
    # sorted_value  - after sorting based on AoA_Val value part of the score_doc
    sorted_words, sorted_value = sort_dic_on_value(score_doc, field)
    min_val = score_doc[sorted_words[0]][field]
    max_val = score_doc[sorted_words[-1]][field]
    median = get_median(sorted_value) # This is otherwise known as q2
    sub_list_low = list(sorted_value[0:len(sorted_value)/2 + 1])
    sub_list_low[-1] = median
    sub_list_high = list(sorted_value[len(sorted_value)/2:])
    sub_list_high[0] = median
    q1 = get_median(sub_list_low)
    q3 = get_median(sub_list_high)
    five_num_summ["min_val"] = min_val
    five_num_summ["max_val"] = max_val
    five_num_summ["median"] = median
    five_num_summ["q1"] = q1
    five_num_summ["q3"] = q3

    return five_num_summ