import requests
import json
from watson_developer_cloud import AlchemyDataNewsV1
import re
# from news_check.helpers.code.secrets import API_KEY
# from news_check.models import Vibe, Company
import pudb
# from news_check.helpers.data.test_data_lists import test_text, test_titles


#1
def build_api_string(*args, **kwargs):
    api_base = 'https://gateway-a.watsonplatform.net/calls/data/GetNews?'
    for key in kwargs:
        api_base += '&'
        api_base += kwargs[key]
    print(api_base)
    return api_base

#2
def call_api(api_string):
    r = requests.get(api_string)
    return r

#3
def build_multi_company_query_param(my_str):
    """
    takes a string like 'jeff is cool'
    and makes it like 'A[jeff^is^cool]'
    cuz thats how alchemy needs it
    """
    my_lst = my_str.split()
    alchemy_str = 'A['
    for i in range(len(my_lst)):
        alchemy_str += my_lst[i]
        if i != len(my_lst) - 1:
            alchemy_str += '^'
    alchemy_str += ']'
    return alchemy_str

#4
def get_api_string_by_keyword(keyword):
    keyword = build_multi_company_query_param(keyword) if ' ' in keyword else keyword
    my_dict = {}
    my_dict['output'] = 'outputMode=json'
    my_dict['start'] = 'start=now-30d'
    my_dict['end'] = 'end=now'
    my_dict['count'] = 'count=10'
    my_dict['query'] = 'q.enriched.url.enrichedTitle.entities.entity=|text=' + keyword + ',type=company|'
    my_dict['return_data'] = 'return=enriched.url.url,enriched.url.title,enriched.url.text,enriched.url.keywords'
    my_dict['apikey'] = 'apikey=' + API_KEY
    return my_dict

#5
def convert_str_to_dict(my_json):
    r = json.loads(my_json.text)
    return r

#6
def run_api(company_name):
    """
    returns a json object from api with title, text, and keywords for
    10 most recent articles about a company
    """
    my_dict = get_api_string_by_keyword(company_name)
    api_str = build_api_string(**my_dict)
    json_str = call_api(api_str)
    r = convert_str_to_dict(json_str)
    return r

#7
def read_txt(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    return data

#8
def parse_json(my_json):
    """
    takes a json object
    returns dictionary containing
    titles: list of with elements of strings of titles
    texts: list of elements of strings of texts
    keywords: garble
    """
    if 'result' in my_json:
        if 'docs' in my_json['result']:
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
    else:
        return False

#9
def strip_string(my_str):
    string = re.sub(r'[^a-zA-Z0-9: ]', '', my_str)
    return string

#10
def strip_list(my_list):
    my_list = [strip_string(lst) for lst in my_list]
    return my_list

#11
def split_strings_into_words(my_list):
    lists = [x.split() for x in my_list]
    words = [item for sublist in lists for item in sublist]
    return words

#12
def get_texts(my_json):
    """
    takes json object with text key and list of texts as strings
    returns just list of words in all texts
    """
    texts = strip_list(my_json['texts'])
    texts = split_strings_into_words(texts)
    return texts

#13
def get_titles(my_json):
    """
    takes json object with text key and list of texts as strings
    returns just list of words in all texts
    """
    titles = strip_list(my_json['titles'])
    titles = split_strings_into_words(titles)
    return titles

#14
def run_api_parse_json(company):
    """
    return dict of data if successful
    else returns False
    """
    my_json = run_api(company)
    parsed = parse_json(my_json)
    return parsed

#15
def text_and_title_for_company(company):
    # gets company data as dict
    parsed_json = run_api_parse_json(company)
    if parsed_json:
        # gets words from article text as list
        text = get_texts(parsed_json)
        # gets words from article titles as list
        titles = get_titles(parsed_json)
        # print("titles" + str(titles))
        # print("\n\n\n\n\n\n")
        # print("text" + str(text))
        # print("\n\n\n\n\n\n")
        return {'text': text, 'titles': titles}
    else:
        return False

#16
def get_words(filename):
    """
    take a file and returns
    all the words in that file
    assuming one word per line
    """
    emotion_words = []
    with open(filename, "r") as words:
        for word in words.readlines():
            emotion_words.append(word.rstrip())
    return emotion_words

#17
def check_emotion(words, emotion):
    count = 0
    for word in words:
        if word in emotion:
            count += 1
    return count

#18
def update_company(company):
    """
    this is the real engine of this thing
    takes a company
    gets happy and sad count of words
    from titles and text
    """
    # get text and title via api call
    words = text_and_title_for_company(company)
    # alternate method for testing it to get text from test data
    if words:
        # build happy and sad words
        happy = get_words('news_check/helpers/data/happy.txt')
        sad = get_words('news_check/helpers/data/sad.txt')
        # get count of happy words for text
        happy_text_count = check_emotion(words['text'], happy)
        # get count of happy words for title
        happy_title_count = check_emotion(words['titles'], happy)
        # get count of sad words for text
        sad_text_count = check_emotion(words['text'], sad)
        # get count of sad words for title
        sad_title_count = check_emotion(words['titles'], sad)
        # get company from db
        company = Company.objects.get(full_name=company)
        # make new vibe
        vibe = Vibe(
            happy_text_count=happy_text_count,
            happy_title_count=happy_title_count,
            sad_text_count=sad_text_count,
            sad_title_count=sad_title_count
        )
        # add company to vibe
        vibe.company = company
        # save
        vibe.save()
    else:
        print('failed to find company with watson')

#19
def get_api_by_pip():
    alchemy_data_news = AlchemyDataNewsV1(api_key='76cba35232ea666b22a856d1150c71978eab16be')

    results = alchemy_data_news.get_news_documents(start='now-2d', end='now')
    print("fox")
    print(json.dumps(results, indent=2))

    results = alchemy_data_news.get_news_documents(
        start='1453334400',
        end='1454022000',
        return_fields=[
            'enriched.url.title',
            'enriched.url.url',
            'enriched.url.text'],
        query_fields={
            'q.enriched.url.enrichedTitle.entities.entity':
            '|text=amazon,type=company|'})
    print("emily")
    print(json.dumps(results, indent=2))




# get_api_by_pip()
# build api string
    # get_api_string_by_keyword
    # build_api_string

# call api
    # call_api

# handle response
    # convert_str_to_dict
    # parse_json

# extract data from response
    # loop_over_companies_and_get_json

# my_json = read_txt('test_data_str.json')
# my_json = parse_json(my_json)
# titles = get_titles(my_json)
# texts = get_text(my_json)
# print(titles)
