# import lib
import os
import re
import nltk
import openpyxl
import pandas as pd
from bs4 import BeautifulSoup
import urllib3
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import cmudict

nltk.download('cmudict')
nltk.download('stopwords')

text_dir = 'P:\\job\\work\\assignment'

#function to create txt file and add text in the file
def file_create_write(f_name, f_title, f_text):
    file = open("%s.txt" % f_name, 'w', encoding="utf-8")
    file.write(f_title)
    # file.write("\n")
    file.write(f_text)
    file.close()


def article_extract(url):
    #requesting html to read
    if not url:
        print("url is empty")
    else:
        page = requests.get(url).text

    # reading text from the article
    soup = BeautifulSoup(page, "html.parser")
    title = soup.title.text.strip() \
        if soup.title \
        else "Untitled"
    body = soup.find_all('div', {"class": "td-post-content tagdiv-type"})

    for ele in body:
        body_text = ele.text

    # print(title,"\ntitle:",type(title), "\nbody:",type(body_text))
    return title, body_text


def file_create(urls, url_ids):

    for n in range(len(url_ids)):
        article_text = ""
        article_title, article_text = article_extract(urls[n])
        file_create_write(url_ids[n], article_title, article_text)
        print(f"{url_ids[n]} file created and text added from {urls[n]}")


def stop_word():
    stop_words = []
    folder_path = os.path.join(text_dir, 'StopWords')

    for file_name in os.listdir(folder_path):
        if 'StopWords' in file_name and file_name.endswith('.txt'):
            file_path_sw = os.path.join(folder_path, file_name)

            with open(file_path_sw, 'r') as file:
                stop_word_list = file.read().split()
                exclude_character = '|'
                stop_word_list = [''.join(char for char in string if char != exclude_character) for string in
                                  stop_word_list]
                stop_word_list = [string for string in stop_word_list if string.strip() != ""]
                stop_words = stop_words + stop_word_list

    return stop_words

def clean_count(texts, r_text):
    text_list = word_tokenize(texts)
    texts_string_lower = [word.lower() for word in text_list]
    words_to_remove_lower = [word.lower() for word in r_text]

    for word in words_to_remove_lower:
        if word in texts_string_lower:
            cleaned_list = [word if word != r_text else " " for word in texts_string_lower]
            cleaned_list = [word for word in cleaned_list if word.isalpha()]

    return cleaned_list, len(cleaned_list)


def clean_text(text_str, stop_word_list):
    text_list = word_tokenize(text_str)
    texts_string_lower = [word.lower() for word in text_list]
    words_to_remove_lower = [word.lower() for word in stop_word_list]

    for word in words_to_remove_lower:
        if word in texts_string_lower:
            cleaned_list = [word if word != stop_word_list else " " for word in texts_string_lower]
            cleaned_list = [word for word in cleaned_list if word.isalpha()]

    return cleaned_list


def master_dictionary():

    folder_path = os.path.join(text_dir, 'MasterDictionary')
    dict = {}
    master_dict = {'positive': [],
                   'negative': []}

    #adding all word in a dict
    for file_name in os.listdir(folder_path):
        if 'positive' in file_name and file_name.endswith('.txt'):
            file_path_pos_md = os.path.join(folder_path, file_name)

            with open(file_path_pos_md, 'r') as file:
                pos = file.read()
                dict["pos"] = file.read()

        if 'negative' in file_name and file_name.endswith('.txt'):
            file_path_neg_md = os.path.join(folder_path, file_name)

            with open(file_path_neg_md, 'r') as file:
                neg = file.read()
                dict["neg"] = file.read()

    stop_words = stop_word()

    master_dict['positive'].append(clean_text(pos, stop_words))
    master_dict['negative'].append(clean_text(neg, stop_words))
    return master_dict

master_dict = master_dictionary()


def extract_derived_variable(text_str):
    stop_words = stop_word()
    master_dict = master_dictionary()
    pos_score = len(master_dict['positive'][0])
    neg_score = len(master_dict['negative'][0])
    polarity_score = round((pos_score - neg_score) / ((pos_score + neg_score) + 0.000001), 4)
    subjectivity_score = round((pos_score + neg_score) / (len(clean_text(text_str, stop_words)) + 0.000001),4)

    return pos_score, neg_score, polarity_score, subjectivity_score

def complex_word_count(text_str):
    input = word_tokenize(text_str)
    vowels = "aeiou"
    syllable_count_list = []
    for i in range(len(input)):
        word = input[i]
        if word.endswith("es"):
            input[i] = word[:-2]
        elif word.endswith("ed"):
            input[i] = word[:-2]

    for w in input:
        syllable_count_list.append(sum(1 for char in w if char.lower() in vowels))

    complex_count_list = [num for num in syllable_count_list if num > 2]
    return len(complex_count_list)

def analysis_of_readability(text_str):
    words = text_str.split()
    words = [word for word in words if word.isalpha()]
    sentences = text_str.split('.')
    avg_snts_len = len(words) / len(sentences)
    percentage_complex_words = complex_word_count(text_str) / len(words)
    fog_index = 0.4 * (avg_snts_len + percentage_complex_words)

    return round(fog_index, 4), round(avg_snts_len, 4), round(percentage_complex_words, 4)


def avg_sentence_length(text_str):
    words = text_str.split()
    words = [word for word in words if word.isalpha()]
    sentences = text_str.split('.')
    avg_snts_len = len(words) / len(sentences)
    return avg_snts_len


def syllable_per_wordd(text_str):
    input = word_tokenize(text_str)
    vowels = "aeiou"
    syllable_count_list = []
    for i in range(len(input)):
        word = input[i]
        if word.endswith("es"):
            input[i] = word[:-2]
        elif word.endswith("ed"):
            input[i] = word[:-2]

    for w in input:
        syllable_count_list.append(sum(1 for char in w if char.lower() in vowels))

    # print(syllable_count_list)
    syllable_count_list = [num for num in syllable_count_list if num > 2]
    return len(syllable_count_list)


def count_personal_pronouns(file):
    with open(os.path.join(text_dir, file), 'r', encoding="utf8") as f:
        text = f.read()
        personal_pronouns = ["I", "we", "my", "ours", "us"]
        count = 0
        for pronoun in personal_pronouns:
            count += len(re.findall(r"\b" + pronoun + r"\b", text))  # \b is used to match word boundaries
    return count


def read_file_return_str(file_name):
    return open(file_name, encoding="utf8").read()


def words_length(file):
    with open(os.path.join(text_dir, file), 'r', encoding="utf8") as f:
        text = re.sub(r'[^\w\s]', '', f.read())
        words = [word for word in text.split()]
        length = sum(len(word) for word in words)
        average_word_length = length / len(words)
    return average_word_length



#creating a dict to add data
data = {'URL_ID': [],
        'URL': [],
        'POSITIVE SCORE': [],
        'NEGATIVE SCORE': [],
        'POLARITY SCORE': [],
        'SUBJECTIVITY SCORE': [],
        'AVG SENTENCE LENGTH': [],
        'PERCENTAGE OF COMPLEX WORDS': [],
        'FOG INDEXS': [],
        'AVG NUMBER OF WORDS PER SENTENCE': [],
        'COMPLEX WORD COUNT': [],
        'WORD COUNT': [],
        'SYLLABLE PER WORD': [],
        'PERSONAL PRONOUNS': [],
        'AVG WORD LENGTH': []}

#reading file
df = pd.read_excel('Input.xlsx')
url_ids = df['URL_ID']
urls = df['URL']

#calling function to create txt files
file_create(urls, url_ids)


#adding url and its id
url_id = []
url = []
for index in urls:
    data['URL'].append(index)
for index in url_ids:
    data['URL_ID'].append(index)

#adding scores
for file_name in os.listdir(text_dir):
    if file_name.endswith('.txt'):
        pos_sc, neg_sc, pol_sc, sub_sc = extract_derived_variable(open(file_name, encoding="utf8").read())
        data['POSITIVE SCORE'].append(pos_sc)
        data['NEGATIVE SCORE'].append(neg_sc)
        data['POLARITY SCORE'].append(pol_sc)
        data['SUBJECTIVITY SCORE'].append(sub_sc)

# adding value for analysis of readability
for file_name in os.listdir(text_dir):
    if file_name.endswith('.txt'):
        avg_sl, fog_i, perc_cw = analysis_of_readability(read_file_return_str(file_name))
        data['AVG SENTENCE LENGTH'].append(avg_sl)
        data['PERCENTAGE OF COMPLEX WORDS'].append(perc_cw)
        data['FOG INDEXS'].append(fog_i)

#avg number of words in a ssentencce
for file_name in os.listdir(text_dir):
    if file_name.endswith('.txt'):
        data['AVG NUMBER OF WORDS PER SENTENCE'].append(avg_sentence_length(read_file_return_str(file_name)))

#cccounting complex sentence
comp_count = []
for file_name in os.listdir(text_dir):
    if file_name.endswith('.txt'):
        data['COMPLEX WORD COUNT'].append(complex_word_count(read_file_return_str(file_name)))

#counting words in article
remove_words = list(stopwords.words('english'))
remove_words.extend(['?','!', ',', '.'])
for file_name in os.listdir(text_dir):
    if file_name.endswith('.txt'):
        words, count=(clean_count(read_file_return_str(file_name), remove_words))
        data['WORD COUNT'].append(count)

#syllable in a word
for file_name in os.listdir(text_dir):
    if file_name.endswith('.txt'):
        data['SYLLABLE PER WORD'].append(syllable_per_wordd(read_file_return_str(file_name)))

#personal pronouns
for file_name in os.listdir(text_dir):
    if file_name.endswith('.txt'):
        data['PERSONAL PRONOUNS'].append(count_personal_pronouns(file_name))

#avg length of word
for file_name in os.listdir(text_dir):
    if file_name.endswith('.txt'):
        data['AVG WORD LENGTH'].append(words_length(file_name))

df = pd.DataFrame(data)
df.to_excel("output.xlsx", index=False)
print("file created")

