import os
import json
import requests
from requests_oauthlib import OAuth1Session
import config


search_url = "https://api.twitter.com/2/tweets/search/recent"

# query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}
query_params = {'query': 'ラファエル','tweet.fields': 'author_id,created_at'}


def get_datas():
    twitter = OAuth1Session(config.CONSUMER_KEY, config.CONSUMER_KEY_SECRET, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    url = f"https://api.twitter.com/2/users/{config.MY_ID}/tweets"
    params = {
        'expansions': 'author_id',
        'tweet.fields': 'created_at,public_metrics',
        'user.fields': 'name',
        'max_results': 5}
    res = twitter.get(url, params=params)

    if res.status_code == 200:
        tl = json.loads(res.text)
        print(f"name : {tl['includes']['users'][0]['name']}")
        print(f"user : {tl['includes']['users'][0]['username']}")
        print('----------------------------')
        for l in tl['data']:
            print(l['text'])
            print(l['created_at'])
            print('----------------------------')
    else:
        print("Failed: %d" % res.status_code)


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {config.BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True, ensure_ascii=False))
    #get_datas()


if __name__ == "__main__":
    main()

