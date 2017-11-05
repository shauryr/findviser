# encoding=utf8
import glob
import json
import math
import os.path
import pickle
import re
from collections import Counter

import textract
import watson_developer_cloud.natural_language_understanding.features.v1 as Features
from watson_developer_cloud import NaturalLanguageUnderstandingV1

import scrap


def get_text_from_pdf(file_path):
    text = textract.process(file_path)
    text = str(text)
    return text


path = 'C:\\Users\\Mukund\\Downloads\\findMyAdvisor\\findMyAdvisor\\data\\'
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-27',
    username='dfcd8207-3f34-411b-b149-7351921f3e1c',
    password='MiQ4T0mHWmKK')


def save_obj(obj, name):
    print('save_obj')
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    print('load_obj')
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


# TODO change path
def get_features_prof():
    list_profs = glob.glob("C:\\Users\\Mukund\\Downloads\\findMyAdvisor\\findMyAdvisor\\prof_pages\\*")
    dict_prof_bow = {}
    dict_prof_concept = {}
    for profs in list_profs:

        with open(profs, 'r') as myfile:
            data = myfile.read()
            try:
                response = natural_language_understanding.analyze(
                    text=data,
                    features=[Features.Entities(), Features.Keywords(), Features.Concepts()])

                keywords = response["keywords"]
                entities = response["entities"]
                concepts = response["concepts"]
                bag_of_words = set()
                concept_set = set()
                for type in [keywords, entities, concepts]:
                    for item in type:
                        bag_of_words.add(item["text"].lower())
                for type in [concepts]:
                    for item in type:
                        concept_set.add(item["text"].lower())

                dict_prof_bow[profs.split('/')[-1]] = ' '.join(list(bag_of_words))
                dict_prof_concept[profs.split('/')[-1]] = ' '.join(list(concept_set))
            except:
                continue
    return dict_prof_bow, dict_prof_concept


def get_features_resume(text):
    data = text
    try:
        response = natural_language_understanding.analyze(
            text=data,
            features=[Features.Entities(), Features.Keywords(), Features.Concepts()])

        keywords = response["keywords"]
        entities = response["entities"]
        concepts = response["concepts"]

        bag_of_words = set()
        for type in [keywords, entities, concepts]:
            for item in type:
                bag_of_words.add(item["text"])

        return ' '.join(list(bag_of_words)).lower()
    except:
        return 'No Resume Found'


WORD = re.compile(r'\w+')


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def return_cosine(text1, text2):
    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    cosine = get_cosine(vector1, vector2)
    return cosine


def get_top_n_prof(n, dict_prof_bow, feature_resume):
    list_recommended_prof = []
    for prof in dict_prof_bow:
        text1 = dict_prof_bow[prof]
        text2 = feature_resume
        list_recommended_prof.append((return_cosine(text1, text2), prof))

    list_recommended_prof.sort(key=lambda tup: tup[0])
    return sorted(list_recommended_prof, reverse=True)[:n]


def get_names_prof(list_recommended_prof):
    list_profs = []
    for _, j in list_recommended_prof:
        list_profs.append(j)
    return list_profs


if os.path.exists(path + "prof_bow.pkl"):
    print("FILE FOUND")
    dict_prof_bow = load_obj(path + "prof_bow")
    dict_prof_concept = load_obj(path + "prof_concept")
else:
    print("FILE NOT FOUND")
    dict_prof_bow, dict_prof_concept = get_features_prof()
    save_obj(dict_prof_bow, path + "prof_bow")
    save_obj(dict_prof_concept, path + "prof_concept")


def return_json(path_to_file):
    txt = get_text_from_pdf(path_to_file)

    feature_resume = get_features_resume(txt)

    list_recommended_prof = get_top_n_prof(5, dict_prof_bow, feature_resume)
    dict_prof_page = load_obj(path + 'dict_prof_page')
    dict_prof_cite = load_obj(path + 'dict_prof_cite')
    dict_cite = {}
    dict_link = {}
    dict_image = {}
    dict_affiliation = {}
    list_name_ordered = []
    #print
    for i in get_names_prof(list_recommended_prof):
        # dict_result[]
        list_name_ordered.append(i)
        dict_link[i] = dict_prof_page[i]
        dict_cite[i] = dict_prof_cite[i]
        dict_image[i] = scrap.dict_prof_images[i]
        dict_affiliation[i] = scrap.dict_prof_affiliation[i].replace('\n', 'ppppp')

    dict_result = {'list_name_ordered': list_name_ordered, 'dict_affiliation': dict_affiliation,
                   'dict_image': dict_image,
                   'dict_link': dict_link, 'dict_cite': dict_cite}

    # print dict_result
    print(dict_result)
    json_data = json.dumps(dict_result)
    json.dump(dict_result, open(path + "json_data.json", 'w'))
    return json_data
