import trials.utils as utils
import json
import trials.drawGraph as drawGraph


def analyze_usr_scr(movie_id, usr_resp):
    with open("data/"+ movie_id+ ".json") as fd:
        mov_scr = json.load(fd)
    movie_det_scr = mov_scr["asset1"]["det_mov_scr"]
    usr_freq_lst = []
    usr_aoa_lst = []
    for word in usr_resp:
        usr_aoa_lst.append(movie_det_scr[word]["AoA"])
        usr_freq_lst.append(movie_det_scr[word]["Freq"])
    usr_aoa_lst.sort()
    usr_freq_lst.sort()
    # aoa_med = utils.get_median(usr_aoa_lst)
    # freq_med = utils.get_median(usr_freq_lst)
    aoa_summ = utils.get_five_num_summary(usr_aoa_lst, "AoA")
    freq_summ = utils.get_five_num_summary(usr_freq_lst, "Freq")
    # drawGraph.plot_graph(mov_scr["asset1"]["det_mov_scr"], mov_scr["aoa_out"], mov_scr["freq_out"],
                        #  mov_scr["q1_avg"],
                        #  mov_scr["q2_avg"], mov_scr["q3_avg"],
                        #  mov_scr]["q4_avg"], (freq_med, aoa_med))

    return aoa_summ["q3"], freq_summ["q3"]

