import streamlit as st
import pandas as pd
import asyncio 
from datetime import date, timedelta
import TwitterAPI
import SentimentAnalysis
import TextSplit
import UploadedFile


# ML-Askの10種類の感情
EMOTION_LIST = ['喜', '安', '好', '昂', '怖', '驚', '怒', '厭', '恥', '哀']

# セッション変数が存在しないとき初期化
if 'negaposi_count' not in st.session_state:
    st.session_state['negaposi_count'] = []

if '10_emotion' not in st.session_state:
    st.session_state['10_emotion'] = []
# 日別の感情変化で利用
if 'negaposi_array' not in st.session_state:
    st.session_state['negaposi_array'] = []
# 日別の感情変化で利用
if '10_emotion_array' not in st.session_state:
    st.session_state['10_emotion_array'] = []
# 日別の感情変化で利用
if 'file_name' not in st.session_state:
    st.session_state['file_name'] = []
if 'selected_emotion' not in st.session_state:
    st.session_state['selected_emotion'] = []


# セッション変数の値をリセット
def reset_clicks():
    st.session_state['negaposi_count'] = []
    st.session_state['10_emotion'] = []
    st.session_state['negaposi_array'] = []
    st.session_state['10_emotion_array'] = []
    st.session_state['file_name'] = []

# メインコルーチン関数
async def main():
    st.set_page_config(page_title="Twitter 感情分類アプリ", page_icon="🌟", layout='wide')
    st.header('Twitter　感情分類アプリ')

############ サイドバー検索フォーム ##############

    with st.sidebar.form(key='search_form2'):
        # st.markdown("## Twitter 感情分類アプリ")
        side_search_word = st.text_input('キーワードを入力', 'コロナ')
        # side_search_tweet_negaposi_count = st.number_input('検索ツイート数 (最大500件)', min_value=50, max_value=500, step=10)
        side_tweet_date = st.date_input('日付 (1週間以内)',
         date.today()+timedelta(days=-1),
         min_value=date.today()+timedelta(days=-8),
         max_value=date.today()+timedelta(days=-1),
         )
        # マルチセレクト
        side_selected_emotion = st.multiselect('10種類から感情を選択', EMOTION_LIST, default=EMOTION_LIST)
        side_radio_button = st.radio('選択した感情のうち', ('一部を含む', '全てを含む'), horizontal=True)
        col = st.columns(2)  # ボタンを横並びにするために設定
        sidebar_search_button_pressed = col[0].form_submit_button('検索')
        sidebar_cancel_button_pressed = col[1].form_submit_button('キャンセル', on_click=reset_clicks)

        


############ メイン検索フォーム #############
    with st.expander('アプリの概要と使い方の説明はこちら', expanded=True):
        st.markdown("---")  #区切り線    
        st.markdown('''##### 概要  
    Twitter上の不安を煽るツイートからユーザーを保護するためのアプリです。  
    ツイートを取得して感情分類を行い、ユーザーが選択した感情のツイートを表示することで不安を煽るツイートを見る機会を減少することができます。''')
        st.markdown("---")  #区切り線    
        st.markdown('''##### 直近のツイートを取得して分類する機能の使い方   

###### 1. 検索したいキーワードを入力します。
    AND検索したい場合は半角スペース区切りで入力  
    OR検索したい場合はORで区切って入力（例：コロナ OR オミクロン）

###### 2. 日付を選択します。(例：2022/12/14) 
    日付は1日前から1週間前までの期間を選択できます。  

###### 3. 10種類から感情を選択します。
    これは感情分析ML-Askで分類される以下から選択できます。  
    喜（よろこび）, 安（やすらぎ）, 好（すき）, 昂（たかぶり）, 怖（こわい）, 驚（おどろき）, 怒（いかり）, 厭（いや）, 恥（はじ）, 哀（あわれ）

###### 4. 選択した感情のうち全てを含むか一部を含むを選択します。
    感情分析結果には10種類の感情が1つの場合や複数含まれることがあります。  
    「一部を含む」を選択した場合は選択した感情が1つでも含まれているものを全て表示します。  
    「全てを含む」を選択した場合は選択した感情と完全に一致したものを表示します。  
  

###### 5. 最後に「検索」ボタンを押します。  
    ツイートの検索・取得・感情分析が行われます。  
    処理が完了するまでお待ちください。



''')
        st.markdown("---")  #区切り線 
        st.markdown('''  

##### CSVファイルをアップロードして分析する機能の使い方  
    Google Colaboratory等で、事前に取得したCSVファイル形式のツイートをアップロードすることで感情分析を行うことができます。  
    複数のファイルをアップロードすることで全てのファイル内のネガティブ・ポジティブの個数や10種類の感情の数を調べることができます。
    アップロードが完了したら「CSVファイルを感情分析」ボタンを押すと、感情分析が実行されます。

''')


    with st.form(key='search_form'):

        # テキストボックス
        search_word = st.text_input('キーワードを入力', 'コロナ')
        # 表示ツイート数
        # search_tweet_negaposi_count = st.number_input('検索ツイート数 (最大500件)', min_value=50, max_value=500, step=10)
        # ツイート検索日
        tweet_date = st.date_input('日付 (1週間以内)',
         date.today()+timedelta(days=-1),
         min_value=date.today()+timedelta(days=-8),
         max_value=date.today()+timedelta(days=-1),
         )
        # マルチセレクト
        selected_emotion = st.multiselect('10種類から感情を選択', EMOTION_LIST, default=EMOTION_LIST)
        radio_button = st.radio('選択した感情のうち', ('一部を含む', '全てを含む'), horizontal=True)



        # ツイートの検索・キャンセルボタン
        col = st.columns(5)  # ボタンを横並びにするために設定
        search_button_pressed = col[0].form_submit_button('検索')
        cancel_button_pressed = col[1].form_submit_button('キャンセル', on_click=reset_clicks)
        sentiment_analysis_button = col[2].form_submit_button('CSVファイルを感情分析')
        uploaded_files = st.file_uploader('CSVファイルをアップロード', type=['csv'], accept_multiple_files=True)
        # search_button_pressed = st.form_submit_button('検索')
        # cancel_button_pressed = st.form_submit_button('キャンセル')




########## メイン検索ボタン #############
  
    if search_button_pressed and search_word and selected_emotion:

        # 検索ボタンが押された時の処理
        with st.spinner(f'{tweet_date}の{search_word}に関する{",".join(selected_emotion)}の感情を含むツイートを検索中...'):
            print('検索ボタンが押されました')
            TwitterAPI.search_word = search_word
            TwitterAPI.fetch_date = tweet_date
            TwitterAPI.fetch_tweet()
            print('ツイート取得完了')
        with st.spinner('感情分析中...'):
            SentimentAnalysis.fileDate = tweet_date
            SentimentAnalysis.main()
            print('感情分析完了')
            TextSplit.fileDate = tweet_date
            TextSplit.selected_emotion = selected_emotion
            TextSplit.radio_button = radio_button
            TextSplit.main()
            print('感情分類できないツイートの除去完了')
            st.success("Success!")
            # st.snow()  # 雪を降らせる
            print(st.session_state['10_emotion'])

        with st.expander('実行結果についての説明はこちら', expanded=True):
            st.markdown("---")  #区切り線
            st.markdown('''  
##### 直近のツイートを取得して分類する機能の実行結果について  

###### 1. 感情分布のグラフについて
    取得したツイートに含まれるネガティブ・ポジティブ分析（左図）と10種類の感情分析の結果（右図）が表示されます。
    各図を選択するとツイート数が表示されます。  
    検索したキーワードで取得されるツイートの感情の分布を知ることができるため、例えばネガティブなツイートが多い場合は、
    事前にツイートを見ないようにすることで不安の軽減が期待できます。

###### 2. 感情分類結果について
    「tweet」、「emotion」、「orientation」の3項目が表示されます。  
    1つ目の「tweet」は、キーワードを入力して検索したツイートのうち、選択された10種類の感情が含まれるツイートのみ表示されます。  
    2つ目の「emotion」は、取得したツイートの10種類の感情分析結果が表示されます。  
    3つ目の「orientation」は、取得したツイートのネガティブ・ポジティブ分析結果が表示されます。
''')


        # グラフの表示(テスト)        
        st.markdown("---")  #区切り線    
        st.subheader(f'{search_word}の感情分布')
        df2 = pd.DataFrame(st.session_state['10_emotion'], columns=['10種類の感情分析'], index=['喜', '安', '好', '昂', '怖', '驚', '怒', '厭', '恥', '哀'])
        # df2 = pd.DataFrame(np.random.rand(20,10), columns=['喜', '安', '好', '昂', '怖', '驚', '怒', '厭', '恥', '哀'])
        col = st.columns(2)

        # Graph (Pie Chart in Sidebar)
        df = pd.DataFrame(st.session_state['negaposi_count'],
                columns=['ネガティブ・ポジティブ分析'],
                index=['概ねネガティブ', '概ねポジティブ', 'ネガティブ', 'ニュートラル', 'ポジティブ'])
        # st.dataframe(df)
        col[0].bar_chart(df)
        


        # st.text('line_chart')
        # st.line_chart(df2)
        # st.text('area_chart')
        # st.area_chart(df2)
        col[1].bar_chart(df2)

        




        # 取得したツイートの感情分析結果の表示
        st.markdown("---")  #区切り線
        st.subheader(f'{search_word}の感情分類結果')

        df = pd.read_csv('/Users/soeyamashunsuke/Desktop/streamlit/data/TextSplit_%s.csv' % tweet_date)
        # st.dataframe(df) 
        st.table(df)
    elif search_button_pressed:
        st.error('エラー：入力内容が不足しています')





########### サイドバー検索ボタン ###############

    if sidebar_search_button_pressed and side_search_word and side_selected_emotion:
        # サイドバーの検索ボタンが押された時の処理
        with st.sidebar:
            with st.spinner(f'{side_tweet_date}の{side_search_word}に関する{",".join(side_selected_emotion)}の感情を含むツイートを検索中...'):
                print('検索ボタンが押されました')
                TwitterAPI.search_word = side_search_word
                TwitterAPI.fetch_date = side_tweet_date
                TwitterAPI.fetch_tweet()
                print('ツイート取得完了')
            with st.spinner('感情分析中'):
                SentimentAnalysis.fileDate = side_tweet_date
                SentimentAnalysis.main()
                print('感情分析完了')
                TextSplit.fileDate = side_tweet_date
                TextSplit.selected_emotion = side_selected_emotion
                TextSplit.radio_button = side_radio_button
                TextSplit.main()
                print('感情分類できないツイートの除去完了')
                # st.success("Success!")
                # st.snow()  # 雪を降らせる
        with st.expander('実行結果についての説明はこちら', expanded=True):
            st.markdown('''

##### 直近のツイートを取得して分類する機能の実行結果について  

###### 1. 感情分布のグラフについて
    取得したツイートに含まれるネガティブ・ポジティブ分析（左図）と10種類の感情分析の結果（右図）が表示されます。
    各図を選択するとツイート数が表示されます。  
    検索したキーワードで取得されるツイートの感情の分布を知ることができるため、例えばネガティブなツイートが多い場合は、
    事前にツイートを見ないようにすることで不安の軽減が期待できます。

###### 2. 感情分類結果について
    「tweet」、「emotion」、「orientation」の3項目が表示されます。  
    1つ目の「tweet」は、キーワードを入力して検索したツイートのうち、選択された10種類の感情が含まれるツイートのみ表示されます。  
    2つ目の「emotion」は、取得したツイートの10種類の感情分析結果が表示されます。  
    3つ目の「orientation」は、取得したツイートのネガティブ・ポジティブ分析結果が表示されます。
''')
            

        # グラフの表示(テスト)        
        st.markdown("---")  #区切り線    
        st.subheader(f'{side_search_word}の感情分布')
        df2 = pd.DataFrame(st.session_state['10_emotion'], columns=['10種類の感情分析'], index=['喜', '安', '好', '昂', '怖', '驚', '怒', '厭', '恥', '哀'])
        # df2 = pd.DataFrame(np.random.rand(20,10), columns=['喜', '安', '好', '昂', '怖', '驚', '怒', '厭', '恥', '哀'])
        col = st.columns(2)
        # Graph (Pie Chart in Sidebar)
        df = pd.DataFrame(st.session_state['negaposi_count'],
        columns=['ネガティブ・ポジティブ分析'],
        index=['概ねネガティブ', '概ねポジティブ', 'ネガティブ', 'ニュートラル', 'ポジティブ'])
        # st.dataframe(df)
        # st.bar_chart(df, height=350)
        col[0].bar_chart(df)


        # st.text('line_chart')
        # st.line_chart(df2)
        # st.text('area_chart')
        # st.area_chart(df2)
        col[1].bar_chart(df2)


        # 取得したツイートの感情分析結果の表示
        st.markdown("---")  #区切り線
        st.subheader(f'{side_search_word}の感情分類結果')
        df = pd.read_csv('/Users/soeyamashunsuke/Desktop/streamlit/data/TextSplit_%s.csv' % side_tweet_date)
        # st.dataframe(df) 
        st.table(df)

    elif sidebar_search_button_pressed:
        st.sidebar.error('エラー：入力内容が不足しています')





########### CSVファイルを感情分析ボタン #############

    if sentiment_analysis_button and uploaded_files:
        # CSVファイルを感情分析ボタンが押された時
        for file in uploaded_files:
            with st.spinner(f'{file.name}を感情分析中...'):
                df = pd.read_csv(file)
                csv = df.to_csv(index=False)
                UploadedFile.csv_data = csv
                UploadedFile.file_name = file.name.lstrip('twitterAPI_')
                UploadedFile.main()
        
        st.success("Success!")

        print('10種類の感情', st.session_state['10_emotion'])
        print('ネガポジ分析', st.session_state['negaposi_count'])
        print('10種類の感情配列', st.session_state['10_emotion_array'])
        print('ネガポジ分析配列', st.session_state['negaposi_array'])

        with st.expander('実行結果についての説明はこちら', expanded=True):
            st.markdown("---")  #区切り線
            st.markdown('''
##### CSVファイルをアップロードして分析する機能の実行結果について 
###### 1. 感情分布のグラフについて
    上記の直近のツイートを取得して分類する機能と同様で、アップロードした全てのファイルの感情分布が表示されます。  

###### 2. 日別の感情変化について
    棒グラフで日別の感情変化を可視化することができます。  
    1つの棒グラフが1つのファイルに含まれる10種類の感情の数になっています。  
    アップロードするファイルが多いほど比較しやすくなります。

''')   
        # グラフの表示       
        st.markdown("---")  #区切り線    
        st.subheader('アップロードした全てのファイルの感情分布')
        df2 = pd.DataFrame(st.session_state['10_emotion'], columns=['10種類の感情分析'], index=['喜', '安', '好', '昂', '怖', '驚', '怒', '厭', '恥', '哀'])
        # df2 = pd.DataFrame(np.random.rand(20,10), columns=['喜', '安', '好', '昂', '怖', '驚', '怒', '厭', '恥', '哀'])
        col = st.columns(2)
        # Graph (Pie Chart in Sidebar)
        df = pd.DataFrame(st.session_state['negaposi_count'],
        columns=['ネガティブ・ポジティブ分析'],
        index=['概ねネガティブ', '概ねポジティブ', 'ネガティブ', 'ニュートラル', 'ポジティブ'])
        # st.dataframe(df)
        # st.bar_chart(df, height=350)
        col[0].bar_chart(df)


        # st.text('line_chart')
        # st.line_chart(df2)
        # st.text('area_chart')
        # st.area_chart(df2)
        col[1].bar_chart(df2)

        # グラフのindexをファイル名の日付で表示
        index_name = []
        for name in st.session_state['file_name']:
            index_name += [name]

        st.markdown("---")  #区切り線    
        st.subheader('日別の感情変化')
        df3 = pd.DataFrame(st.session_state['negaposi_array'],
        columns=['概ねネガティブ', '概ねポジティブ', 'ネガティブ', 'ニュートラル', 'ポジティブ'],
        index=index_name
        )
        st.bar_chart(df3)
        # print(st.session_state['file_name'][0])
        print(index_name)
        reset_clicks()
    elif sentiment_analysis_button:
        st.error('CSVファイルがアップロードされていません。')

   


########### キャンセルボタン ############

    if cancel_button_pressed or sidebar_cancel_button_pressed:
        # キャンセルボタンが押された時の処理
        reset_clicks()
        print('キャンセルボタンが押されました')
        st.experimental_rerun()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    