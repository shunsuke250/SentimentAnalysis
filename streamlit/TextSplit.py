import pandas as pd
import csv
import streamlit as st

fileDate = '' # ファイルの日付を指定
selected_emotion = [] # 10種類の感情を指定
radio_button = '' # 全てを含むか一部を含むかの選択

def main():
    
    path = '/Users/soeyamashunsuke/Desktop/streamlit/data/App_%s.csv' % fileDate

    data_list = []
    selected_emotion_label = []

    positive_count = 0
    mostly_positive_count = 0
    negative_count = 0
    mostly_negative_count = 0
    neutral_count = 0

    yorokobi_count = 0
    yasu_count = 0
    suki_count = 0
    takaburi_count = 0
    kowa_count = 0
    odoroki_count = 0
    ikari_count = 0
    iya_count = 0
    haji_count = 0
    aware_count = 0

    for emotion in selected_emotion:
        selected_emotion_label += [int(str(emotion).replace('厭', '7').replace('喜', '0').replace('怖', '4').replace('安', '1').replace('好', '2').replace('哀', '9').replace('怒', '6').replace('驚', '5').replace('昂', '3').replace('恥', '8'))]
    
    
    with open (path) as f:
        reader = csv.reader(f) # 一行ずつ読み込む

        for row in reader:
            emotion_label = []
            if row[2] != "":
                del row[0]
                del row[3:8]
                if row[1] == 'emotion':
                    data_list.append(row)
                else:
                    row[1] = row[1][29:]
                    row[1] = row[1][:-2]
                    row[1] = row[1].replace('iya', '厭').replace('yorokobi', '喜').replace('kowa', '怖').replace('yasu', '安').replace('suki', '好').replace('aware', '哀').replace('ikari', '怒').replace('odoroki', '驚').replace('takaburi', '昂').replace('haji', '恥')
                    
                    if '喜' in row[1]:
                        emotion_label += [0]
                        yorokobi_count += 1
                    if '安' in row[1]:
                        emotion_label += [1]
                        yasu_count += 1
                    if '好' in row[1]:
                        emotion_label += [2]
                        suki_count += 1
                    if '昂' in row[1]:
                        emotion_label += [3]
                        takaburi_count += 1
                    if '怖' in row[1]:
                        emotion_label += [4]
                        kowa_count += 1
                    if '驚' in row[1]:
                        emotion_label += [5]
                        odoroki_count += 1
                    if '怒' in row[1]:
                        emotion_label += [6]
                        ikari_count += 1
                    if '厭' in row[1]:
                        emotion_label += [7]
                        iya_count += 1
                    if '恥' in row[1]:
                        emotion_label += [8]
                        haji_count += 1
                    if '哀' in row[1]:
                        emotion_label += [9]
                        aware_count += 1

                    # orientation列のネガポジの個数を計算
                    if row[2] == 'POSITIVE':
                        positive_count += 1
                    elif row[2] == 'mostly_POSITIVE':
                        mostly_positive_count += 1
                    elif row[2] == 'NEGATIVE':
                        negative_count += 1
                    elif row[2] == 'mostly_NEGATIVE':
                        mostly_negative_count += 1
                    elif row[2] == 'NEUTRAL':
                        neutral_count += 1


                    # emotion列の10種類の選択された感情を含むツイートを保存
                    if radio_button == '全てを含む':
                        if set(selected_emotion_label) == set(emotion_label):
                            data_list.append(row)
                            # print(selected_emotion_label)
                    if radio_button == '一部を含む':
                        for i in selected_emotion_label:
                            if i in emotion_label:
                                data_list.append(row)

                    # print(emotion_label, selected_emotion_label)
    
    
    st.session_state['negaposi_count'] = [mostly_negative_count, mostly_positive_count, negative_count, neutral_count, positive_count]
    st.session_state['10_emotion'] = [yorokobi_count, yasu_count, suki_count, takaburi_count, kowa_count, odoroki_count, ikari_count, iya_count, haji_count, aware_count]

    f.close()


    df = pd.DataFrame(data_list)
    df.to_csv('/Users/soeyamashunsuke/Desktop/streamlit/data/TextSplit_%s.csv' % fileDate, encoding='utf-8-sig', header=False, index=False)



file_name = ''

def uploaded_file():

    path = '/Users/soeyamashunsuke/Desktop/streamlit/data/App_%s' % file_name

    data_list = []
    selected_emotion_label = []

    positive_count = 0
    mostly_positive_count = 0
    negative_count = 0
    mostly_negative_count = 0
    neutral_count = 0

    yorokobi_count = 0
    yasu_count = 0
    suki_count = 0
    takaburi_count = 0
    kowa_count = 0
    odoroki_count = 0
    ikari_count = 0
    iya_count = 0
    haji_count = 0
    aware_count = 0

    for emotion in selected_emotion:
        selected_emotion_label += [int(str(emotion).replace('厭', '7').replace('喜', '0').replace('怖', '4').replace('安', '1').replace('好', '2').replace('哀', '9').replace('怒', '6').replace('驚', '5').replace('昂', '3').replace('恥', '8'))]
    
    
    with open (path) as f:
        reader = csv.reader(f) # 一行ずつ読み込む

        for row in reader:
            emotion_label = []
            if row[5] != "":
                del row[0:4]
                del row[3:8]
                if row[1] == 'emotion':
                    data_list.append(row)
                else:
                    row[1] = row[1][29:]
                    row[1] = row[1][:-2]
                    row[1] = row[1].replace('iya', '厭').replace('yorokobi', '喜').replace('kowa', '怖').replace('yasu', '安').replace('suki', '好').replace('aware', '哀').replace('ikari', '怒').replace('odoroki', '驚').replace('takaburi', '昂').replace('haji', '恥')
                    
                    if '喜' in row[1]:
                        emotion_label += [0]
                        yorokobi_count += 1
                    if '安' in row[1]:
                        emotion_label += [1]
                        yasu_count += 1
                    if '好' in row[1]:
                        emotion_label += [2]
                        suki_count += 1
                    if '昂' in row[1]:
                        emotion_label += [3]
                        takaburi_count += 1
                    if '怖' in row[1]:
                        emotion_label += [4]
                        kowa_count += 1
                    if '驚' in row[1]:
                        emotion_label += [5]
                        odoroki_count += 1
                    if '怒' in row[1]:
                        emotion_label += [6]
                        ikari_count += 1
                    if '厭' in row[1]:
                        emotion_label += [7]
                        iya_count += 1
                    if '恥' in row[1]:
                        emotion_label += [8]
                        haji_count += 1
                    if '哀' in row[1]:
                        emotion_label += [9]
                        aware_count += 1

                    # orientation列のネガポジの個数を計算
                    if row[2] == 'POSITIVE':
                        positive_count += 1
                    elif row[2] == 'mostly_POSITIVE':
                        mostly_positive_count += 1
                    elif row[2] == 'NEGATIVE':
                        negative_count += 1
                    elif row[2] == 'mostly_NEGATIVE':
                        mostly_negative_count += 1
                    elif row[2] == 'NEUTRAL':
                        neutral_count += 1


                    # emotion列の10種類の選択された感情を含むツイートを保存
                    # if radio_button == '全てを含む':
                    #     if set(selected_emotion_label) == set(emotion_label):
                    #         data_list.append(row)
                    #         # print(selected_emotion_label)
                    # if radio_button == '一部を含む':
                    #     for i in selected_emotion_label:
                    #         if i in emotion_label:
                    #             data_list.append(row)


                    data_list.append(row)
            

                    # print(emotion_label, selected_emotion_label)
    
    
    st.session_state['negaposi_count'] = [mostly_negative_count, mostly_positive_count, negative_count, neutral_count, positive_count]
    st.session_state['10_emotion'] = [yorokobi_count, yasu_count, suki_count, takaburi_count, kowa_count, odoroki_count, ikari_count, iya_count, haji_count, aware_count]

    f.close()


    df = pd.DataFrame(data_list)
    df.to_csv('/Users/soeyamashunsuke/Desktop/streamlit/data/TextSplit_%s' % file_name, encoding='utf-8-sig', header=False, index=False)
