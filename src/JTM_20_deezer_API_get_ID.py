import re
import pandas as pd
import deezer
import time
import requests

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\JTMpartial.xlsx', sheet_name='SongDB')

    print(df_all.tail())

    # dropping duplicated values
    subset = ['Song_correct', 'Artist_correct']
    df_all.drop_duplicates(subset=subset, keep=False, inplace=True)

    # reseting index
    df_all.reset_index(drop=True, inplace=True)

    print(df_all.tail())

    df_all["Search"] = df_all.apply(lambda df: deezer_search(df['Artist_correct'], df['Song_correct']), axis=1)

    # # unpacking tuple form first search
    # df_all["Song_ID"] = df_all['Search'].apply(lambda df: df[0])

    # saving to excel file
    print('saving file')
    df_all.to_csv(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\20_ListaPiosenekDezeerID.csv',
                    index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

def deezer_search(search_value_1, search_value_2):
    try:
        url = "https://api.deezer.com/search?q=artist:'{value1}' track:'{value2}'".format(value1=search_value_1, value2=search_value_2)
        search_result = requests.get(url).json()
        song_id = search_result['data'][0]['id']
        print(song_id)
        # song = search_result['data'][0]['title']
        # artist = search_result['data'][0]['artist']['name']
    except IndexError:
        song_id = ""
    except ValueError:
        song_id = ""
    return song_id

if __name__ == "__main__":
    main()


