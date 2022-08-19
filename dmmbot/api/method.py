import requests
import json
import re
import random

from .. import CONFIG

URL_BASE = 'https://api.dmm.com/affiliate/v3/ItemList'

PARAMS_BASE = {
        'api_id': CONFIG['DMM']['api_id'],
        'affiliate_id': CONFIG['DMM']['affiliate_id'],
        'site': 'FANZA',
        'service': 'digital',
        'floor': 'videoa',
        'sort': 'date',
        'output': 'json'
        }

def get_preview(cid):
    r = requests.get(f"https://www.dmm.co.jp/service/digitalapi/-/html5_player/=/cid={cid}/mtype=CARdWwNE/")
    s = re.search('{"bitrate":3000.+mp4"}', r.text)
    if not s:
        return None
    s = s.group(0)
    url = f"https:{json.loads(s)['src']}"
    return url

def search(keyword):
    params = PARAMS_BASE.copy()
    params['keyword'] = keyword
    result = requests.get(URL_BASE, params=params).json()
    return result['result']['items']

def movie_info(cid):
    params = PARAMS_BASE.copy()
    params['cid'] = cid
    result = requests.get(URL_BASE, params=params).json()
    return result['result']['items'][0]

def random_results():
    params = PARAMS_BASE.copy()
    params['offset'] = str(random.randint(1, 50000))
    result = requests.get(URL_BASE, params=params).json()
    return result['result']['items']
