import streamlit as st
import tweepy
import csv
from collections import namedtuple
from datetime import timedelta # 日本時間に直すために使用

search_word = ''
fetch_date = ''

def fetch_tweet():

    api_key = st.secrets.TwitterAPI.api_key
    api_secret = st.secrets.TwitterAPI.api_secret
    access_token = st.secrets.TwitterAPI.access_token
    access_secret = st.secrets.TwitterAPI.access_secret

    auth = tweepy.OAuthHandler(api_key,api_secret)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True) # ツイート取得の制限になった場合に15分中断する

    word = '-bot -RT %s　since:%s_00:00:00_JST until:%s_23:59:59_JST' % (search_word, fetch_date, fetch_date)
    maxid = 0

    # f = open('twitterAPI_%s.csv' % fetch_date, 'w',encoding='UTF-8')
    with open('/Users/soeyamashunsuke/Desktop/streamlit/data/twitterAPI_%s.csv' % fetch_date, 'w',encoding='UTF-8') as f:
        tweet_data_list = []

        while len(tweet_data_list) < 1000:
            result = api.search_tweets(q=word, lang='ja', count=100, max_id=maxid)
            print(len(result))
            if len(result)==0:
                break
            for res in result:
                maxid = res.id-1
                sc_name = res.user.screen_name # @ユーザー名
                name = res.user.name # プロフィール名
                desc = res.user.description # 自己紹介文
                text = res.text.replace('\n', '') # ツイート文
                datetime = res.created_at + timedelta(hours=9) #　日本時間に変換
                location = res.place # 位置情報

                if 'bot' in name.lower() or 'bot' in desc.lower(): # 紹介文と名前にBOTを除く
                    continue
                elif 'PaperbackNew' in sc_name: # PaperbackNew（ユーザー名）のツイートは取り除けない改行文字があるため除く
                    continue
                elif 'Covid19Nara' in sc_name: # Covid19Nara（ユーザー名）のツイートは取り除けない改行文字があるため除く
                    continue
                elif 'ScienceBookNew' in sc_name:
                    continue  
                elif 'iHerb' in text: # iHerb最新クーポン紹介botを除く
                    continue

                tweet_data_list.append([f'{text}'])

            print(datetime)

        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["text"])
        writer.writerows(tweet_data_list)


