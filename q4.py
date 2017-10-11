import pandas as pd
word_dict = {}
tag_name = "WORDTAG"
tag_dict = {}
emission_probablity_dict = word_dict
def training_dict():
    data = open("a1_datasets/q4_UD_English/train.counts","r")
    lines = list(data)
    # print lines
    pos = {}
    for line in lines:
        item = line.split()
        if item[1] == tag_name:
            if len(item) == 4:
                # Tag dictionary
                item[2] = item[2].lower()
                if not item[2] in tag_dict.keys():
                    tag_dict[item[2]] = int(item[0])
                else:
                    tag_dict[item[2]] += int(item[0])

                # Word Dictionary
                item[3] = item[3].lower()
                if not item[3] in word_dict.keys():
                    pos[item[2]] = int(item[0])
                    word_dict[item[3]] = pos

                else:
                    if not item[2] in word_dict[item[3]].keys():
                        pos[item[2]] = int(item[0])
                        word_dict[item[3]][item[2]] = pos[item[2]]
                    else:
                        word_dict[item[3]][item[2]] = word_dict[item[3]][item[2]] + int(item[0])
                    # item[2]] = word_dict[item[3]][item[2]] + item[0]
                    # print word_dict[item[3]][item[2]]
                pos = {}
        # print word_dict

def emission_probablity(word_dict):
    # print tag_dict

    for item in word_dict.keys():
        for tag in word_dict[item].keys():
            numerator = float(word_dict[item][tag])
            denominator = float(tag_dict[tag])
            probability = float(numerator / denominator)
            emission_probablity_dict[item][tag] = probability

    # print emission_probablity_dict
    for key, value in emission_probablity_dict.iteritems():
        print key , value









if __name__ == "__main__":
    training_dict()
    emission_probablity(word_dict)

