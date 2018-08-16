from random import randint
import trials.utils as utils
import math
def get_avg_scr(pop_list):
    val = 0
    for elem in pop_list:
        val += elem
    return val/len(pop_list)


def get_tgt_scr_index(tgt_lst, tgt_scr):
    idx = 0

    for elem in tgt_lst:
        if elem >= tgt_scr:
            return idx
        else:
            idx +=1
    if idx >= len(tgt_lst):
        return None
    else:
        return idx


def stratified_sampler(sorted_pop, sample_size):
    sample_list = []
    index_list = []
    pop_copy = sorted_pop[:]
    print("orig pop size:", len(sorted_pop), " copy pop size:", len(pop_copy))

    avg_scr = get_avg_scr(sorted_pop)
    # this returns the index which is closer to the avg_scr
    avg_idx = get_tgt_scr_index(sorted_pop, avg_scr)

    print("avg_scr:", avg_scr, "avg_idx:", avg_idx)
    sample_list.append(sorted_pop[0])
    pop_copy[0] = 0
    sample_list.append(sorted_pop[-1])
    pop_copy[-1] = 0
    while len(sample_list) < sample_size:
        sample_avg = get_avg_scr(sample_list)
        if sample_avg <= avg_scr:
            rand_idx = randint(avg_idx, len(sorted_pop) - 1)
            print("random index:", rand_idx)
            if pop_copy[rand_idx] == 0:
                continue
            else:
                sample_list.append(sorted_pop[rand_idx])
                pop_copy[rand_idx] = 0
                index_list.append(rand_idx)
        else:
            rand_idx = randint(0, avg_idx)
            if pop_copy[rand_idx] == 0:
                continue
            else:
                sample_list.append(sorted_pop[rand_idx])
                pop_copy[rand_idx] = 0
                index_list.append(rand_idx)

    sample_list.sort()
    index_list.sort()
    return sample_list, index_list


def get_quad_med_scr(quad_data):

    freq_scr = [float(val['Freq']) for val in quad_data.values()]
    aoa_scr = [float(val['AoA']) for val in quad_data.values()]
    freq_scr.sort()
    aoa_scr.sort()
    freq_med = utils.get_median(freq_scr)
    aoa_med = utils.get_median(aoa_scr)

    return freq_med, aoa_med


def get_quad_data(dic):
    q1_data = {}
    q2_data = {}
    q3_data = {}
    q4_data = {}

    q1_data = {k: v for k, v in dic.items() if v["Quad"] == "q1"}
    q2_data = {k: v for k, v in dic.items() if v["Quad"] == "q2"}
    q3_data = {k: v for k, v in dic.items() if v["Quad"] == "q3"}
    q4_data = {k: v for k, v in dic.items() if v["Quad"] == "q4"}

    print("Q1 Data:\n", q1_data)
    print("Q2 Data:\n", q2_data)
    print("Q3 Data:\n", q3_data)
    print("Q4 Data:\n", q4_data)

    return q1_data, q2_data, q3_data, q4_data


def get_dist_from_med(word_det, med_scr):
    # med_scr (freq_val, aoa_val)
    dist = math.sqrt(math.pow((med_scr[0] - word_det["Freq"]), 2) + math.pow((med_scr[1] - word_det["AoA"]), 2))
    return dist


def get_sample_from_quad(quad_data, med_scr, samp_size, min_quota):
    for word in quad_data:
        dist = get_dist_from_med(quad_data[word], med_scr)
        quad_data[word]["Dist"] = dist

    wrd_lst, dist_lst = utils.sort_dic_on_value(quad_data, "Dist")
    print("Distance of each word from its median:")
    # for word in wrd_lst:
    #     print word, quad_data[word]
    if samp_size < min_quota and len(quad_data) > min_quota:
        samp_size = min_quota
    elif len(quad_data) < samp_size:
        samp_size = len(quad_data)

    samp_lst = wrd_lst[:samp_size]

    return samp_lst


def four_cluster_sampling(detailed_dic, sample_size=4, min_quota=2):

    q1_data, q2_data, q3_data, q4_data = get_quad_data(detailed_dic)
    q1_avg_scr = get_quad_med_scr(q1_data)
    q2_avg_scr = get_quad_med_scr(q2_data)
    q3_avg_scr = get_quad_med_scr(q3_data)
    q4_avg_scr = get_quad_med_scr(q4_data)
    print("q1 avg scr:", q1_avg_scr, " q2 avg scr:", q2_avg_scr, " q3 avg scr:", q3_avg_scr, " q4 avg scr:", q4_avg_scr)
    q1_samp = get_sample_from_quad(q1_data, q1_avg_scr, sample_size, min_quota)
    q2_samp = get_sample_from_quad(q2_data, q2_avg_scr, sample_size, min_quota)
    q3_samp = get_sample_from_quad(q3_data, q3_avg_scr, sample_size, min_quota)
    q4_samp = get_sample_from_quad(q4_data, q4_avg_scr, sample_size, min_quota)
    print("Q1 Samples:", q1_samp)
    print("Q2 Samples:", q2_samp)
    print("Q3 Samples:", q3_samp)
    print("Q4 Samples:", q4_samp)
    samples_lst = q1_samp + q2_samp + q3_samp + q4_samp

    return samples_lst, q1_avg_scr, q2_avg_scr, q3_avg_scr, q4_avg_scr


if __name__ == "__main__":
    a = [14, 42, 32, 45, 35, 56, 77, 18, 59, 10, 33, 21, 1, 4, 14, 36, 37, 59, 67, 24]
    a.sort()
    print(a)
    samp_lst, idx_lst = stratified_sampler(a, 7)
    print("Sample List:", samp_lst, "Samp Avg:", get_avg_scr(samp_lst), " selected Index:", idx_lst)
