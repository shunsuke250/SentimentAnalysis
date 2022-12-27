import SentimentAnalysis
import TextSplit


file_name = ''
csv_data = ''


def main():

    with open('/Users/soeyamashunsuke/Desktop/streamlit/data/%s' % file_name, 'w', encoding='UTF-8') as f:
        
        f.write(csv_data)

    SentimentAnalysis.file_name = file_name
    SentimentAnalysis.uploaded_analysis()
    TextSplit.file_name = file_name
    TextSplit.uploaded_file()
    


