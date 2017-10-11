from itertools import count

import nltk, re, pprint
import pandas as pd
from nltk import word_tokenize

def replace_unknowns_bigrams(data_text, wordcount_dict):
    # print wordcount_dict
    data_text = list(data_text)
    words = []
    data_text_processed = []                        # Stores data with UNK replaced.
    for item_index, item in enumerate(data_text):
        words = item.split()
        for index, word in enumerate(words):
            count = wordcount_dict[word]
            if(count < 5 ):
                words[index] = 'UNK'
                data_text_list = data_text[item_index].split()
        if len(words) == 1:
            str = words[0]
            data_text_processed.append('<s> '+str+ ' </s>')
        else:
            str = ""
            for w in words:
                str = str +" " +w
            data_text_processed.append('<s>' + str+ ' </s>')
    create_bigram_count(data_text_processed)
    return data_text_processed

def replace_unknowns(data_text, wordcount_dict):
    # print wordcount_dict
    data_text = list(data_text)
    words = []
    data_text_processed = []                        # Stores data with UNK replaced.
    for item_index, item in enumerate(data_text):
        words = item.split()
        for index, word in enumerate(words):
            count = wordcount_dict[word]
            if(count < 5 ):
                words[index] = 'UNK'
                data_text_list = data_text[item_index].split()
        if len(words) == 1:
            str = words[0]
            data_text_processed.append('<s> <s> '+str+ ' </s>')
        else:
            str = ""
            for w in words:
                str = str +" " +w
            data_text_processed.append('<s> <s>' + str+ ' </s>')
    # print data_text_processed
    # create_trigram_count(data_text_processed)
    # create_bigram_count(data_text_processed)
    # for item in data_text_processed:
    #     print item
    # print data_text_processed
    create_unigram_count(data_text_processed)
    return data_text_processed

def create_unigram_count(data_text):
    unigram_dict = {}
    for sentence in data_text:
        words = sentence.split()
        for word in words:
            if not word in unigram_dict:
                unigram_dict[word] = 1
            else:
                unigram_dict[word] += 1
    count_of_unigrams = unigram_dict.keys()

    print "Length of vocabulary : ", len(count_of_unigrams)
    return unigram_dict

def create_trigram_count(data_text):
    trigram_dict = {}
    # print data_text
    for sentence in data_text:
        sentence_split = sentence.split()
        for index , word in enumerate(sentence_split):
            try:
                first = sentence_split[index]
                second = sentence_split[index + 1]
                third = sentence_split[index + 2]
                if third != 'null':
                    str = first + " "+ second+ " "+ third
                    # print str
                    if not str in trigram_dict:
                        trigram_dict[str] = 1
                    else:
                        trigram_dict[str] += 1
            except IndexError:
                break
    # for key,value in trigram_dict.items():
    #     print key, value
    # print trigram_dict
    return trigram_dict
    # print len(trigram_dict)
    # for key,value in trigram_dict.items():
    #     print key, value
    # trigram_probability(trigram_dict)

def create_bigram_count(data_text):
    bigram_dict = {}
    # print data_text
    for sentence in data_text:
        sentence_split = sentence.split()
        for index , word in enumerate(sentence_split):
            try:
                first = sentence_split[index]
                second = sentence_split[index + 1]
                if second != 'null':
                    str = first + " "+ second
                    # print str
                    if not str in bigram_dict:
                        bigram_dict[str] = 1
                    else:
                        bigram_dict[str] += 1
            except IndexError:
                break
    # for k, v in bigram_dict.iteritems():
    #     print k, v
    return bigram_dict

    # print len(trigram_dict)
    # for key,value in bigram_dict.items():
    #     print key, value
    # trigram_probability(trigram_dict)


def trigram_probability_add1(trigram_dict):
    total_trigram_words = 0
    # for key , value in trigram_dict.items():
    #     total_trigram_words = total_trigram_words+ trigram_dict[key]
    total_trigram_words = trigram_dict.keys()
    # print len(total_trigram_words)
    return len(total_trigram_words)


def add1_smoothing(unigram_count, data_text_training):
    data = pd.read_csv("a1_datasets/q3_lm/test_set.csv",
                       sep=",")
    data['text'] = data['text'].map(lambda x: re.sub('\{.', "", x.strip().lower()))
    # data['text'] = data['text'].map(lambda x: re.sub(ur'[^a-zA-Z0-9\' ,*\u2019]', '', x))
    data['text'] = data['text'].map(lambda x: re.sub(ur'[^A-Za-z0-9\']+', ' ', x))
    data['text'] = data['text'].replace(",", "")
    data_text_test = data['text']
    data_text_test = list(data_text_test)
    # Training data with 'UNK'

    data_text_training = list(data_text_training)
    training_trigram_dict = create_trigram_count(data_text_training)

    # training_bigram_dict = create_bigram_count(data_text_training_bigrams)
    training_bigram_dict = create_bigram_count(data_text_training)

    test_data_text_processed =[]
    # Adding start and end tags to the test data
    for item in data_text_test:
        words = item.split()
        # print words
        if len(words) == 1:
            str = words[0]
            test_data_text_processed.append('<s> <s> '+str+ ' </s>')
        else:
            str = ""
            for w in words:
                str = str +" " +w
            test_data_text_processed.append('<s> <s>' + str+ ' </s>')


    # print data_text

    vocabulary = trigram_probability_add1(training_trigram_dict)
    # print vocabulary
    sum = 0.0
    for sentence in test_data_text_processed:
        trigram_probability_after_smoothing = 1
        sentence_split = sentence.split()
        length = len(sentence_split)
        for index, word in enumerate(sentence_split):
            try:
                first = sentence_split[index]
                second = sentence_split[index + 1]
                third = sentence_split[index + 2]
                if third != 'null':
                    str = first + " " + second + " " + third
                    bigram_string = first + " " + second
                    # print str
                    try:
                        # print bigram_string
                        count_of_trigram = training_trigram_dict[str]
                        count_of_bigrams = training_bigram_dict[bigram_string]
                    except KeyError:
                        count_of_trigram = 0.0
                        count_of_bigrams = 0.0
                    # print count_of_bigrams

                    # 6103 is found out in the function create_unigram_count()
                    denominator = float(count_of_bigrams + 6103)
                    numerator = (count_of_trigram + 1.0)
                    trigram_probability_after_smoothing *= float(numerator/denominator)

            except IndexError:
                break
        sum += (1 / trigram_probability_after_smoothing) ** (1.0 / length)
    average = sum/len(test_data_text_processed)
    print "Perplexity :", average
        # print (1/trigram_probability_after_smoothing) ** (1/N)
        #print trigram_probability_after_smoothing



if __name__ == "__main__":
    data = pd.read_csv("a1_datasets/q3_lm/train_set.csv",
                       sep=",")
    data['text'] = data['text'].map(lambda x: re.sub('\{.', "", x.strip().lower()))
    # data['text'] = data['text'].map(lambda x: re.sub(ur'[^a-zA-Z0-9\' ,*\u2019]', '', x))
    data['text'] = data['text'].map(lambda x: re.sub(r'\<.*>+', '', x))
    data['text'] = data['text'].map(lambda x: re.sub(ur'[^A-Za-z0-9\']+', ' ', x))

    data['text'] = data['text'].replace(",","")

    # Regular expression trials
    # str = "{Dhow, <ar'e> you?}"
    # str = re.sub('\{.',"",str)
    # str = re.sub(r'\<.*>+', "", str)
    # str = re.sub('[^A-Za-z0-9\']+'," ",str)
    #
    # print str
    # data['text'] = data['text'].map(lambda x: re.sub('[^A-Za-z0-9]+', ' ', x.strip().lower()))


    # Unigram count for each word. Doing this to replace words with frequency < 5 with UNK
    data_text = data['text']
    unigram_count = {}
    for word in data_text:
        listOfWords = re.findall(r'\S+', word)
        for eachWord in listOfWords:
            if not eachWord in unigram_count:
                unigram_count[eachWord] = 1
            else:
                unigram_count[eachWord] += 1
    # unigram_count = create_unigram_count()
    # print unigram_count
    # print eachWord
    # print data_text
    # print d.keys()
    # print len(d)
    data_text_training = replace_unknowns(data_text,unigram_count);
    # data_text_training_bigrams = replace_unknowns_bigrams(data_text,unigram_count)
    # create_trigram_count(data_text)
    # create_bigram_count(data_text)
    # trigramsProbability()
    # add1_smoothing(unigram_count, data_text_training, data_text_training_bigrams)
    add1_smoothing(unigram_count, data_text_training)