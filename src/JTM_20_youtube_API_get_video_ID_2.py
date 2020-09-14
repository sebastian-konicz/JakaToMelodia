from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import selenium
from googleapiclient.discovery import build

PATH = 'C:\Users\kose9001\Desktop\JTM'

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\interim\Lista_piosenek_youtube.xlsx')
    print(df_all.head())

    # concatenating song and artist for youtube search
    df_all["Song_concat"] = df_all.apply(lambda df: df['Song_correct'] + " " + df['Artist_correct'], axis=1)

    # getting youtube video id
    df_all["YT_id"] = df_all.apply(lambda df: youtube_search(df['Song_concat']), axis=1)

    # link to the song
    df_all["YT_link"] = df_all.apply(lambda df: "https://www.youtube.com/watch?v=" + df["YT_id"], axis=1)

    # saving to excel file
    print('saving file')
    df_all.to_csv(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\20_ListaPiosenekYoutube.csv',
                    index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

def youtube_search(search_value):
    try:
        print(str(search_value))

        api_key = JTM_0_config.api_key

        youtube = build('youtube', 'v3', developerKey=api_key)

        request = youtube.search().list(
            part="snippet",
            maxResults=3,
            q=str(search_value))

        response = request.execute()

        song_id = response['items'][0]['id']['videoId']
        # song_title = response['items'][0]['snippet']['title']

        print(response['items'][0]['id']['videoId'])
        # print(response['items'][0]['snippet']['title'])

    except IndexError:
        song_id = ""
    except ValueError:
        song_id = ""
    return song_id

if __name__ == "__main__":
    main()


