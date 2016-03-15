import requests
import json
import re
import pudb
from news_check.helpers.code.secrets import API_KEY
from news_check.models import Vibe, Company
from watson_developer_cloud import AlchemyDataNewsV1, watson_developer_cloud_service
from textblob import TextBlob


class GetApi:
    """
    source must be "txt", "api", or "pip"
    company is needed for "api" and "pip"
    returns json str to get sent to TextTitle
    """
    def __init__(self, source, company=None, txt_file=None):
        self.source = source
        # self.variables = variables
        self.company = company
        self.txt_file = txt_file

    def run_api(self):
        if self.source == "api":
            return self.get_api()
        elif self.source == "txt":
            return self.read_txt()
        elif self.source == "pip":
            return self.get_pip()
        else:
            raise ValueError('invalid source argument')

    # 6
    def get_api(self):
        """
        returns a json object from api with title, text, and keywords for
        10 most recent articles about a company
        """
        api = ApiHelpers()
        my_dict = api.get_api_string_by_keyword(self.company)
        api_str = api.build_api_string(**my_dict)
        json_str = api.call_api(api_str)
        r = api.convert_str_to_dict(json_str.text)
        return r

    # 7
    def read_txt(self):
        with open(self.txt_file) as data_file:
            data = json.load(data_file)
        return data

    # 19
    def get_pip(self):
        api = ApiHelpers()
        alchemy_data_news = AlchemyDataNewsV1(api_key='76cba35232ea666b22a856d1150c71978eab16be')
        if ' ' in self.company:
            api = ApiHelpers()
            self.company = api.build_multi_company_query_param(self.company) if ' ' in self.company else self.company
        results = alchemy_data_news.get_news_documents(
            start='1453334400',
            end='1454022000',
            return_fields=[
                'enriched.url.title',
                'enriched.url.url',
                'enriched.url.text'],
            query_fields={
                'q.enriched.url.enrichedTitle.entities.entity':
                '|text=' + self.company + ',type=company|'})
        return api.convert_str_to_dict(json.dumps(results, indent=2))


class ApiHelpers:

    def __init__(self):
        pass

    # 1
    def build_api_string(*args, **kwargs):
        api_base = 'https://gateway-a.watsonplatform.net/calls/data/GetNews?'
        for key in kwargs:
            api_base += '&'
            api_base += kwargs[key]
        print(api_base)
        return api_base

    # 2
    def call_api(self, api_string):
        r = requests.get(api_string)
        return r

    # 3
    def build_multi_company_query_param(self, my_str):
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

    # 4
    def get_api_string_by_keyword(self, keyword):
        keyword = self.build_multi_company_query_param(keyword) if ' ' in keyword else keyword
        my_dict = {}
        my_dict['output'] = 'outputMode=json'
        my_dict['start'] = 'start=now-30d'
        my_dict['end'] = 'end=now'
        my_dict['count'] = 'count=10'
        my_dict['query'] = 'q.enriched.url.enrichedTitle.entities.entity=|text='
        my_dict['query'] += keyword + ',type=company|'
        my_dict['return_data'] = 'return=enriched.url.url,enriched.url.title,enriched.url.text'  # ,enriched.url.keywords'
        my_dict['apikey'] = 'apikey=' + API_KEY
        return my_dict

    # 5
    def convert_str_to_dict(self, my_json):
        r = json.loads(my_json)
        return r


class TextTitle:
    """
    returns dict of data
    with text and title
    concatenated together
    as key
    """
    def __init__(self, json_str):
        self.json_str = json_str

    # 8
    def parse_json(self, my_json):
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
                for nugget in data:
                    start = nugget['source']['enriched']['url']
                    texts.append(start['text'])
                    titles.append(start['title'])
                return {'titles': titles, 'texts': texts}
        else:
            return False

    # 9
    def strip_string(self, my_str):
        string = re.sub(r'[^a-zA-Z0-9: ]', '', my_str)
        return string

    # 10
    def strip_list(self, my_list):
        my_list = [self.strip_string(lst) for lst in my_list]
        return my_list

    # 11
    def split_strings_into_words(self, my_list):
        lists = [x.split() for x in my_list]
        words = [item for sublist in lists for item in sublist]
        return words

    # 12
    def get_texts(self, my_json):
        """
        takes json object with text key and list of texts as strings
        returns just list of words in all texts
        """
        texts = self.strip_list(my_json['texts'])
        texts = self.split_strings_into_words(texts)
        return texts

    # 13
    def get_titles(self, my_json):
        """
        takes json object with text key and list of texts as strings
        returns just list of words in all texts
        """
        titles = self.strip_list(my_json['titles'])
        titles = self.split_strings_into_words(titles)
        return titles

    # 15
    def text_and_title_for_company(self):
        # gets company data as dict
        parsed_json = self.parse_json(self.json_str)
        if parsed_json:
            # gets words from article text as list
            text = self.get_texts(parsed_json)
            # gets words from article titles as list
            titles = self.get_titles(parsed_json)
            # print("titles" + str(titles))
            # print("\n\n\n\n\n\n")
            # print("text" + str(text))
            # print("\n\n\n\n\n\n")
            return {'text': text, 'titles': titles}
        else:
            return False


class Algorithm:
    """
    takes dictionary from TextFile
    gets happy and sad text count
    """
    def __init__(self, dictionary, algorithm):
        self.dictionary = dictionary

    # 16
    def get_words(self, filename):
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

    # 17
    def check_emotion(self, words, emotion):
        count = 0
        for word in words:
            if word in emotion:
                count += 1
        return count

    def jeff(self):
        self.happy = self.get_words('news_check/helpers/data/happy.txt')
        self.sad = self.get_words('news_check/helpers/data/sad.txt')
        self.happy_text_count = self.check_emotion(self.dictionary['text'], self.happy)
        self.happy_title_count = self.check_emotion(self.dictionary['titles'], self.happy)
        self.sad_text_count = self.check_emotion(self.dictionary['text'], self.sad)
        self.sad_title_count = self.check_emotion(self.dictionary['titles'], self.sad)

    def text_blob(self):
        text = self.join_words(self.dictionary['text'])
        titles = self.join_words(self.dictionary['titles'])
        self.blob_title_score = TextBlob(text).sentiment.polarity
        self.blob_text_score = TextBlob(titles).sentiment.polarity

    def join_words(self, list_of_words):
        return " ".join(list_of_words)

    # # 18
    # def update_company(self, company):
    #     """
    #     this is the real engine of this thing
    #     takes a company
    #     gets happy and sad count of words
    #     from titles and text
    #     """
    #     words = self.dictionary
    #     # alternate method for testing it to get text from test data
    #     if words:
    #         # build happy and sad words
    #         self.happy = self.get_words('news_check/helpers/data/happy.txt')
    #         self.sad = self.get_words('news_check/helpers/data/sad.txt')
    #         # get count of happy words for text
    #         self.happy_text_count = self.check_emotion(words['text'], happy)
    #         # get count of happy words for title
    #         self.happy_title_count = self.check_emotion(words['titles'], happy)
    #         # get count of sad words for text
    #         self.sad_text_count = self.check_emotion(words['text'], sad)
    #         # get count of sad words for title
    #         self.sad_title_count = self.check_emotion(words['titles'], sad)
    #         # get company from db
    #         company = Company.objects.get(full_name=company)
    #         # make new vibe
    #         vibe = Vibe(
    #             happy_text_count=happy_text_count,
    #             happy_title_count=happy_title_count,
    #             sad_text_count=sad_text_count,
    #             sad_title_count=sad_title_count
    #         )
    #         # add company to vibe
    #         vibe.company = company
    #         # save
    #         vibe.save()
    #     else:
    #         print('failed to find company with watson')


class SaveToDB:
    """
    takes stats from Algorithm
    saves them to db
    if using txt, then you need to pass the company argument
    which should match a company name in the db
    stats must be an object of type Algorithm
    """
    def __init__(self, stats, company):
        self.stats = stats
        self.company = company

    def save_to_db(self):
        company = Company.objects.get(full_name=self.company)
        # make new vibe
        vibe = Vibe(
            happy_text_count=self.stats.happy_text_count,
            happy_title_count=self.stats.happy_title_count,
            sad_text_count=self.stats.sad_text_count,
            sad_title_count=self.stats.sad_title_count,
            blob_title_score=self.stats.blob_title_score,
            blob_text_score=self.stats.blob_text_score
        )
        # add company to vibe
        vibe.company = company
        # save
        vibe.save()


class RunData:
    """
    RunData(source="txt").run()
    RunData(source="pip", company="Allstate").run()
    RunData(source="api", company="Allstate").run()
    """
    def __init__(self, source, company=None, save=False):
        self.source = source
        self.company = company
        self.save = save

    def run(self):
        # get api
        if self.source == "api":
            return self.run_api()
        elif self.source == "txt":
            return self.run_txt()
        elif self.source == "pip":
            return self.run_pip()
        else:
            raise ValueError('invalid source argument')

    def run_txt(self):
        try:
            api = GetApi(source=self.source, txt_file="news_check/helpers/data/test_pip_data.json").run_api()
            text_titles = TextTitle(api).text_and_title_for_company()
            algorithm = Algorithm(text_titles)
            algorithm.jeff()
            algorithm.text_blob()
            if self.save:
                SaveToDB(algorithm, self.company).save_to_db()
            return True
        except Exception as e:
            print(e)
            return False

    def run_pip(self):
        try:
            api = GetApi(source=self.source, company=self.company).run_api()
            text_titles = TextTitle(api).text_and_title_for_company()
            algorithm = Algorithm(text_titles)
            algorithm.jeff()
            algorithm.text_blob()
            if self.save:
                SaveToDB(algorithm, self.company).save_to_db()
            return True
        except watson_developer_cloud_service.WatsonException as e:
            print(e)
            return False

    def run_api(self):
        try:
            api = GetApi(source=self.source, company=self.company).run_api()
            text_titles = TextTitle(api).text_and_title_for_company()
            algorithm = Algorithm(text_titles)
            algorithm.jeff()
            algorithm.text_blob()
            if self.save:
                SaveToDB(algorithm1, self.company).save_to_db()
            return True
        except TypeError as e:
            print(e)
            return False
