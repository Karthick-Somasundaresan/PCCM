import matplotlib.pyplot as plt
import json


def get_individual_lst(det_dic):
    wrd_lst = []
    aoa_lst = []
    freq_lst = []
    for word in det_dic:
        wrd_lst.append(word)
        freq_lst.append(det_dic[word]["Freq"])
        aoa_lst.append(det_dic[word]["AoA"])

    return freq_lst, aoa_lst, wrd_lst



def plot_graph(det_dic, aoa_out, freq_out, q1_m, q2_m, q3_m, q4_m, usr_scr):
    freq_lst, aoa_lst, wrd_list = get_individual_lst(det_dic)
    print("Got individual list")
    fig, ax = plt.subplots()
    print("About to plot graph")
    ax.scatter(aoa_lst, freq_lst, alpha = 0.25)
    print("After to plot graph")

    for i, txt in enumerate(wrd_list):
        ax.annotate(txt, (aoa_lst[i], freq_lst[i]))
    xmin, xmax = ax.get_xbound()
    ymin, ymax = ax.get_ybound()
    plt.plot([xmin, xmax], [freq_out, freq_out], c="red")
    plt.plot([aoa_out, aoa_out], [ymin, ymax], c="red")
    ax.scatter(q1_m[1], q1_m[0], marker="D", c="r", label="Q1 median")
    ax.scatter(q2_m[1], q2_m[0], marker="D", c="m", label="Q2 median")
    ax.scatter(q3_m[1], q3_m[0], marker="D", c="k", label="Q3 median")
    ax.scatter(q4_m[1], q4_m[0], marker="D", c="b", label="Q4 median")
    # ax.(usr_scr[1], usr_scr[0], marker="o", c="b", label="User's Score")
    plt.plot([xmin, xmax], [usr_scr[0], usr_scr[0]], c="b")
    plt.plot([usr_scr[1], usr_scr[1]], [ymin, ymax], c="b")
    plt.xlabel('Age of Acquisition')
    plt.ylabel('Word Frequency')
    plt.title('Word Dispersion')
    #plt.interactive(False)
    plt.legend()
    plt.show()
    print("Showing")

if __name__ == "__main__":
    with open("data/asset1.json") as fp:
        mov_wrd_lst = json.load(fp)
    
    print("mov_wrd_lst:")
    plot_graph(mov_wrd_lst["asset1"]["det_mov_scr"], 11.57, 1.11, (3.382, 6.0), (0.81165, 9.235), (1.6173, 12.5), (0.699, 13.615), (2.5, 7.64))
