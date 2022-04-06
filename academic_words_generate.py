import os
from pathlib import Path
import json

DATA_DIRECTORY = os.path.join(Path(os.getcwd()).absolute(), 'data/')
OUTPUT_DIRECTORY = os.path.join(Path(os.getcwd()).absolute(), 'output/')

'''
    This script reads Averil Coxhead's Academic Words list to store its corresponding tiers, and brings more derived words from its head word from Categorical Variation Dataset (Version 2.1) 
    The final data format is in json.
'''


def add_entry_of_AWL(awl_data, word, is_head_word, tier, current_head_word):
    if tier not in awl_data:
        awl_data[tier] = {}

    if is_head_word:
        awl_data[tier][word] = []
    else:
        awl_data[tier][current_head_word].append(word)


def load_AWL_data():
    tier_capture_line = 'Academic Word List'
    awl_data = {}
    tier = 0

    with open(DATA_DIRECTORY + "AWL.txt", "r") as reader:
        lines = reader.readlines()
        current_head_word = ''
        for line in lines:
            word = line.rstrip()

            if len(word) == 0:
                continue

            if tier_capture_line in word:
                tier += 1
                continue

            if word[0] == '\t':
                is_head_word = False
            else:
                is_head_word = True
                current_head_word = word.strip()

            word = word.strip()
            add_entry_of_AWL(awl_data, word, is_head_word, tier, current_head_word)
    return awl_data


def load_catvar_data():
    clusters = []
    with open(DATA_DIRECTORY + "/catvar21.signed.txt", "r") as reader:
        lines = reader.readlines()
        for line in lines:
            cluster = set()
            words = line.split("#")
            if len(words) > 1:
                for word in words:
                    cluster.add(word[:word.index("_")])
            clusters.append(cluster)
    return clusters

def merge_data(awl_data, clusters):
    for entry in awl_data.values():
        for head_word, sub_words in entry.items():
            for cluster in clusters:
                if head_word in cluster:
                    for word in cluster:
                        if word not in entry[head_word] and word != head_word:
                            entry[head_word].append(word)

def write_to_json(dict_obj):
    with open(OUTPUT_DIRECTORY + 'awl_catvar.json', 'w') as fp:
        json.dump(dict_obj, fp)

awl_data = load_AWL_data()
clusters = load_catvar_data()

merge_data(awl_data, clusters)
write_to_json(awl_data)
