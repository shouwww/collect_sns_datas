import os
import json
import requests
from requests_oauthlib import OAuth1Session
import config
import pandas as pd


search_url = "https://api.twitter.com/2/tweets/search/recent"

# query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}
query_params = {'query': '#2月27日はポケモンデー -is:reply -is:retweet lang:ja','tweet.fields': 'author_id,created_at,id,public_metrics'}
# 検索ワード  e.g. query = "テスト" / query = "テスト OR test"
# OR 検索　AND検索　-検索　などしたい場合はそのように書く

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
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response


def format_data(data):
    ret_datas = []
    ret_dict = {}
    for data_key, data_value in data.items():
            if data_key == 'public_metrics':
                for mykey, myvalue in data_value.items():
                    ret_dict[mykey] = myvalue
                    #ret_datas.append(myvalue)
            else:
                ret_dict[data_key] = data_value
                # ret_datas.append(data_value)
    return ret_dict #ret_datas

def main():
    if not os.path.exists('data'):
        os.mkdir('data')
    dave_csvpath = os.path.join('data','datas.csv')
    header_str = ['text','author_id','id','retweet_count','reply_count','like_count','quote_count','created_at']
    json_response = connect_to_endpoint(search_url, query_params)
    datas_json = json.loads(json_response.text)
    #datas_json = json.dumps(json_response, indent=4, sort_keys=True, ensure_ascii=False)
    keys = datas_json.keys() 
    print(keys)
    datas = datas_json['data']
    print(type(datas))
    for data in datas:
        # ここから一つ一つのデータに分解
        print('============')
        ret = format_data(data)
        print(ret)
        #for key,value in zip (header_str,ret):
        #    print(key,value)


    print('==================================')
    # ファイル読み込み
    df = pd.json_normalize(ret)
    # df.to_csv('datas.csv', index=False, encoding='cp932')    
    old_df = pd.read_csv(dave_csvpath, encoding='cp932')
    
    #new_df =old_df.join(df)
    #print(new_df)
    #df.to_csv('datas.csv', index=False, encoding='cp932')
    print(old_df)
    print(df)
    new_pd = pd.concat([old_df,df])
    print('==================================')
    print(new_pd)
    new_pd.to_csv(dave_csvpath, index=False, encoding='cp932')
    """
        for data_key,data_value in data.items():
            if data_key == 'public_metrics':
                for mykey,myvalue in data_value.items():
                    print(mykey) 
                    print(myvalue)
            else:
                print(data_key)
                print(data_value)

    for data in datas:
        print('============')
        print(data.keys())
        print(data)
        meta_datas = data['public_metrics']
        for mykey,myvalue in meta_datas.items():
            print(mykey) 
            print(myvalue)
    """

    #for key in datas_json['data']:
    #    print('=======================')
    #    print(key)
    #get_datas()


if __name__ == "__main__":
    main()

