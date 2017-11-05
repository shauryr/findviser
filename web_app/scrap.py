# encoding=utf8
import urllib2
from bs4 import BeautifulSoup
import re
import requests
from nltk.tokenize import word_tokenize
import collections
from nltk.corpus import stopwords
import pickle


def save_obj(obj, name):
    print ('save_obj')
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    print ('load_obj')
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


path_data = 'C:\\Users\\Mukund\\Downloads\\findMyAdvisor\\findMyAdvisor\\data\\'
path = 'C:\\Users\\Mukund\\Downloads\\findMyAdvisor\\findMyAdvisor\\prof_pages\\'
ist_url = "https://ist.psu.edu/"
wiki = "https://ist.psu.edu/directory/faculty"

page = urllib2.urlopen(wiki)

soup = BeautifulSoup(page)

links = soup.findAll("td", {'class': "views-field views-field-view-user"})
affiliation = soup.findAll("td", {'class': "views-field views-field-field-title views-align-left"})
image = soup.findAll("td", {'class': "views-field views-field-field-image views-align-right"})
emails = soup.findAll("p")

dict_prof_affiliation = {}
dict_name_links = collections.OrderedDict()

dict_prof_images = {}
# faculty page of IST link dictionary
for i in links:
    dict_name_links[i.h4.text] = ist_url + i.a["href"]

for i, j in zip(affiliation, dict_name_links.keys()):
    dict_prof_affiliation[j] = i.text.rstrip()

for i, j in zip(image, dict_name_links.keys()):
    dict_prof_images[j] = i.img["src"]


def save_prof_citations():
    import scholarly
    dict_prof_cite = {}
    for i in dict_name_links:
        try:
            dict_prof_cite[i] = next(scholarly.search_author(i)).fill().citedby
        except:
            dict_prof_cite[i] = ''
            continue
        print(i)
    save_obj(dict_prof_cite, path_data + 'dict_prof_cite')
    return dict_prof_cite


# save_prof_citations()


def get_dict_prof_page():
    count = 0
    dict_prof_page = {}
    dict_prof_email = {}
    # actual link of faculty's website
    for prof in dict_name_links:
        page = urllib2.urlopen(dict_name_links[prof])
        soup = BeautifulSoup(page)
        print(prof)
        links = soup.find("div", {'class': "views-field views-field-field-web-site-s-"})
        if links:
            dict_prof_page[prof] = links.a["href"]
            count += 1
        else:
            dict_prof_page[prof] = dict_name_links[prof]
    save_obj(dict_prof_page, path_data + 'dict_prof_page')
    return dict_prof_page, dict_prof_email


def write_files(dict_prof_page):
    dict_prof_content_first_page = {}
    for prof in dict_prof_page:
        link = dict_prof_page[prof]
        print(prof)
        try:
            html = requests.get(link).text
        except:
            continue

        """If you do not want to use requests then you can use the following code below 
           with urllib (the snippet above). It should not cause any issue."""
        soup = BeautifulSoup(html, "lxml")
        res = soup.body
        text_content = res.text
        cleaned = " ".join(re.findall('[A-Z][^A-Z]*', text_content))

        tokens = word_tokenize(cleaned)
        # convert to lower case
        tokens = [w.lower() for w in tokens]
        # remove punctuation from each word
        # remove remaining tokens that are not alphabetic
        words = [word for word in tokens if word.isalpha()]
        # filter out stop words
        words = [w for w in words if not w in stop_words]
        dict_prof_content_first_page[prof] = " ".join(words)
    print(dict_prof_content_first_page.__len__())

    for prof in dict_prof_content_first_page:
        print(path + prof, 'WRITING HERE ')
        fil_w = open(path + prof, 'w')
        fil_w.write(dict_prof_content_first_page[prof].encode('utf-8').strip())
        fil_w.close()


if __name__ == '__main__':
    dict_prof_page, dict_prof_email = get_dict_prof_page()
    write_files(dict_prof_page)

    stop_words = stopwords.words('english')
