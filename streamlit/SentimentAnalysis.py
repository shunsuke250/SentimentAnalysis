import pandas as pd
import csv
import tqdm
from mlask import MLAsk
import streamlit as st

fileDate = ''

def main():

    emotion_analyzer = MLAsk()
    
    path = "/Users/soeyamashunsuke/Desktop/streamlit/data/twitterAPI_%s.csv" % fileDate

    original_data = []
    analyzed_data = []
    error_count = 0

    with open (path) as f:
        reader = csv.reader(f) # 一行ずつ読み込む
        for row in reader:
            original_data.append(row)

    for i in tqdm.tqdm(range(1, len(original_data))):
            try:
                result = emotion_analyzer.analyze(original_data[i][0])
                analyzed_data.append(result)
            except:
                print('%s行目：書式が崩れている可能性があります。' % i)
                error_count += 1

    if error_count != 0:
        print('合計%s個のエラーが見つかりました。元データを確認して該当の行を削除してください' % error_count)
        
        
    df = pd.DataFrame(analyzed_data, columns=None)
    # 感情分析結果の保存
    df.to_csv('/Users/soeyamashunsuke/Desktop/streamlit/data/ML-Ask_%s.csv' % fileDate, encoding='utf-8-sig')
    # df.head()

    # 2つのcsvファイルを編集して結合
    df_api = pd.read_csv('/Users/soeyamashunsuke/Desktop/streamlit/data/twitterAPI_%s.csv' % fileDate, encoding='utf-8')
    df_result = pd.read_csv('/Users/soeyamashunsuke/Desktop/streamlit/data/ML-Ask_%s.csv' % fileDate, encoding='utf-8', index_col=0)
    df_result = df_result.drop('text', axis=1)
    df_con = pd.concat([df_api, df_result], axis=1)
    df_con.to_csv('/Users/soeyamashunsuke/Desktop/streamlit/data/App_%s.csv' % fileDate)
    df_con.head()



########### アップロードしたcsvファイルを感情分析 ##############

file_name = ''

def uploaded_analysis():
    
    my_bar = st.progress(0)

    emotion_analyzer = MLAsk()
    
    path = "/Users/soeyamashunsuke/Desktop/streamlit/data/%s" % file_name

    original_data = []
    analyzed_data = []
    error_count = 0

    with open (path) as f:
        reader = csv.reader(f) # 一行ずつ読み込む
        for row in reader:
            original_data.append(row)

        for i in range(1, len(original_data)):
            try:
                result = emotion_analyzer.analyze(original_data[i][3])
                analyzed_data.append(result)
            except:
                print('%s行目：書式が崩れている可能性があります。' % i)
                error_count += 1
            
            my_bar.progress(i/len(original_data))
            print('感情分析中：', int(i/len(original_data)*100), '%')
    my_bar.progress(100)

    if error_count != 0:
        print('合計%s個のエラーが見つかりました。元データを確認して該当の行を削除してください' % error_count)
        
        
    df = pd.DataFrame(analyzed_data, columns=None)
    # 感情分析結果の保存
    df.to_csv('/Users/soeyamashunsuke/Desktop/streamlit/data/ML-Ask_%s' % file_name, encoding='utf-8-sig')
    # df.head()

    # 2つのcsvファイルを編集して結合
    df_api = pd.read_csv('/Users/soeyamashunsuke/Desktop/streamlit/data/%s' % file_name, encoding='utf-8')
    df_result = pd.read_csv('/Users/soeyamashunsuke/Desktop/streamlit/data/ML-Ask_%s' % file_name, encoding='utf-8', index_col=0)
    df_result = df_result.drop('text', axis=1)
    df_con = pd.concat([df_api, df_result], axis=1)
    df_con.to_csv('/Users/soeyamashunsuke/Desktop/streamlit/data/App_%s' % file_name)
    
    # df_con.head()
    
    # 1つのファイルを分析完了時にプログレスバーを非表示
    my_bar.empty()


