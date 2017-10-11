import numpy as np
import q4 as q4
import re
import q4_2 as q4_2
from q4 import emission_probablity_dict
from q4_2 import transition_probablity_dict

word_dict = {}
tags = []

def viterbi_algorithm(trigram_list, transition_dict):
    viterbi = np.zeros((len(tags), len(trigram_list)))
    path_trace = np.zeros((len(tags), len(trigram_list)))
    for tag in range(len(tags)):
        if trigram_list[0] in emission_dict and tags[tag] in transition_dict:
            if '*' in transition_dict[tags[tag]] and tags[tag] in emission_dict[trigram_list[0]]:
                viterbi[tag][0] = transition_dict[tags[tag]]['*'] * emission_dict[trigram_list[0]][tags[tag]]
                path_trace[tag][0] = tag

    print viterbi
    print path_trace

    for indx in range(1, len(trigram_list)):
        for tag_i in range(len(tags)):
            for tag_j in range(len(tags)):
                if trigram_list[indx] in emission_dict and tags[tag_i] in transition_dict:
                    # Viterbi algo comparison
                    if tags[tag_j] in transition_dict[tags[tag_i]] and tags[tag_i] in emission_dict[trigram_list[indx]]:
                        if viterbi[tag_j][indx] < viterbi[tag_j][indx - 1] * transition_dict[tags[tag_i]][tags[tag_j]] * emission_dict[trigram_list[indx]][tags[tag_i]]:
                            viterbi[tag_j][indx] = viterbi[tag_j][indx - 1] * transition_dict[tags[tag_i]][tags[tag_j]] * emission_dict[trigram_list[indx]][tags[tag_i]]
                            path_trace[tag_j][indx] = tag_i

    print viterbi
    print path_trace

if __name__ == "__main__":
    q4.training_dict()
    word_dict = q4.word_dict
    q4.emission_probablity(word_dict)

    q4_2.training_dict()
    word_dict = q4_2.word_dict
    q4_2.transition_probablity(word_dict)

    # tags = transition_probablity_dict.keys()
    emission_dict = emission_probablity_dict
    transition_dict = transition_probablity_dict

    # print 'emission_dict', emission_dict
    # print 'transition_dict' , transition_dict
    data = open("a1_datasets/q4_UD_English/test.tags", "r")

    lines = list(data)
    line = []
    for item in lines:
        try:
            word = item.split()
            tags.append(word[1])
            line.append(word[0])
        except IndexError:
            continue

    data = open("a1_datasets/q4_UD_English/test.words", "r")

    lines = list(data)

    # for item in lines:
    #     item = re.sub(ur'[^A-Za-z0-9\']+', '', item)
    #     line.append(item)
    # line = list(filter(None, line))
    # print line

    for index, item in enumerate(line):
        try:
            if not item[index + 2] is None:
                first = line[index]
                second = line[index + 1]
                third = line[index + 2]
                test_list = [first, second, third]
                viterbi_algorithm(test_list, transition_dict)
        except IndexError:
            break