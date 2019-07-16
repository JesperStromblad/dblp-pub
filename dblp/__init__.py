import pandas as pd
import requests

#options
STRINGS_FOR_TEST = ["Collaborative Writing"]
DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
PUB_SEARCH_URL = DBLP_BASE_URL + "search/publ/api"


def query_db(pub_string=STRINGS_FOR_TEST):
    '''
    returns the Json object of a query to DBLP

    :param pub_string: A list of strings of keywords
    :return: JSON: A JSON Object
    '''
    resp = requests.get(PUB_SEARCH_URL, params={'q':pub_string, 'h': '1000', 'format' : 'json'})

    return resp.json()

def get_pub_data(json):
    '''
    Extracts the information about a publication from a BeautifulSoup object

    :param pub: A JSON Object with Publication Information
    :return: dict: All Information of this Publication
    '''
    list_pub = []
    publication_data = json['result']['hits']['hit']
    for field in publication_data:
        dict_info = {}
        info = field['info']
        if all (key in info for key in ("authors","ee", "title", "type", "venue","year")):  # Some details are not available in dblp e.g., author or venue
            #dict_info['authors'] = info['authors']['author']
            list = info['authors']['author']
            dict_info['authors'] = ','.join(list)
            dict_info['url'] = info['ee']
            dict_info['title'] = info['title']
            dict_info['type'] = info['type']
            dict_info['where'] = info['venue']
            dict_info['year'] = info['year']
        list_pub.append(dict_info)
    return list_pub


def search(search_string=STRINGS_FOR_TEST):
    '''
    returns the information found in a search query to dblp as a pandas dataframe.
    Shows the following information:
        - Authors
        - Link to Publication
        - Title
        - Type (Article, Proceedings etc.)
        - Where it was published
        - Year of publication
    :param search_string: A List of Strings of Keywords, that should be searched for
    :return: pd.DataFrame: A Dataframe with all data
    '''
    json = query_db(search_string)
    pub  = get_pub_data(json)
    return pd.DataFrame(pub)



