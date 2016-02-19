import requests
import pudb
import json
import re, string
from secrets import API_KEY

def build_api_string(*args, **kwargs):
    api_base = 'https://gateway-a.watsonplatform.net/calls/data/GetNews?'
    for key in kwargs:
        api_base += '&'
        api_base += kwargs[key]
    return api_base

def call_api(api_string):
    r = requests.get(api_string)
    return r

def get_api_string_by_keyword(keyword):
    my_dict = {}
    my_dict['output'] = 'outputMode=json'
    my_dict['start'] = 'start=now-30d'
    my_dict['end'] = 'end=now'
    my_dict['count'] = 'count=10'
    my_dict['query'] = 'q.enriched.url.enrichedTitle.entities.entity=|text=' + keyword + ',type=company|'
    my_dict['return_data'] = 'return=enriched.url.url,enriched.url.title,enriched.url.text,enriched.url.keywords'
    my_dict['apikey'] = 'apikey=' + API_KEY
    return my_dict

def convert_str_to_dict(my_json):
    acceptable_str = my_json.text.replace("'", "\"")
    r = json.loads(acceptable_str)
    return r

def run_api():
    '''
    returns a json object from api with title, text, and keywords for
    10 most recent articles about a company
    '''
    my_dict = get_api_string_by_keyword('walmart')
    api_str = build_api_string(**my_dict)
    json_str = call_api(api_str)
    r = convert_str_to_dict(json_str)
    return r

def read_txt(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    return data

def parse_json(my_json):
    '''
    takes a json object
    returns dictionary containing
    titles: list of with elements of strings of titles
    texts: list of elements of strings of texts
    keywords: garble
    '''
    data = my_json['result']['docs']
    titles = []
    texts = []
    keywords = []
    for nugget in data:
        start = nugget['source']['enriched']['url']
        keywords.append(start['keywords'])
        texts.append(start['text'])
        titles.append(start['title'])
    return {'titles': titles, 'texts': texts, 'keywords': keywords}

def strip_string(my_str):
    string = re.sub(r'[^a-zA-Z0-9: ]', '', my_str)
    return string

def strip_list(my_list):
    my_list = [strip_string(lst) for lst in my_list]
    return my_list

def split_strings_into_words(my_list):
    lists = [x.split() for x in my_list]
    words = [item for sublist in lists for item in sublist]
    return words

def get_text(my_json):
    '''
    takes json object with text key and list of texts as strings
    returns just list of words in all texts
    '''
    texts = strip_list(my_json['texts'])
    texts = split_strings_into_words(texts)
    return texts

def get_titles(my_json):
    '''
    takes json object with text key and list of texts as strings
    returns just list of words in all texts
    '''
    titles = strip_list(my_json['titles'])
    titles = split_strings_into_words(titles)
    return titles

my_json = read_txt('test_data_str.json')
my_json = parse_json(my_json)
titles = get_titles(my_json)
texts = get_text(my_json)
print(titles)
print(texts)