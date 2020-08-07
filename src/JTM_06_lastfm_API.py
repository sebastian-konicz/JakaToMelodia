import pandas as pd
import time
import re
import requests
import operator
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# SEARCHING FOR THE CORRECT SONG ARTIST FOR SPLIT_CONCANTENATED BASED ON KNOWN SONGS-ARTIST PAIRS
# AND ASSIGNING SONGS WITH THE HIGHEST TOKEN RATIO > 85
def main():
    # start time of function
    start_time = time.time()

    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\05_ListaPiosenekFuzzy.xlsx')

    # replacing NaN values in dataframe
    df_all["Song_correct"].fillna("", inplace=True)
    df_all["Artist_correct"].fillna("", inplace=True)
    df_all["Song_correct_search"].fillna("", inplace=True)
    df_all["Artist_correct_search"].fillna("", inplace=True)

    # getting correct song/ artist values
    df_all["Song_correct"] = df_all.apply(
        lambda df_all: df_all["Song_correct"] if (df_all["Song_correct"] != "") else df_all["Song_correct_search"], axis=1)
    df_all["Artist_correct"] = df_all.apply(
        lambda df_all: df_all["Artist_correct"] if (df_all["Artist_correct"] != "") else df_all["Artist_correct_search"], axis=1)

    # droping unnecessary columns
    df_all.drop(columns=['Song_correct_search', 'Artist_correct_search'], inplace=True)

    # replacing NaN values in dataframe
    df_all["Song_split"].fillna("", inplace=True)
    df_all["Artist_split"].fillna("", inplace=True)

    # creating new column with concatenated values from song_correct and artist_correct
    df_all["Split_Concatenated"] = df_all.apply(
        lambda df_all: (str(df_all['Song_split']) + " " + str(df_all['Artist_split'])), axis=1)

    # running search on dataframe
    df_all["Search_1"] = df_all.apply(
        lambda df: lastfm_search(df['Split_Concatenated']) if (
                    (df['Song_correct'] == "") | (df['Artist_correct'] == "")) else "", axis=1)

    # unpacking tuple form first search
    df_all["Song_correct_search"] = df_all.apply(
        lambda df: df['Search_1'][1] if ((df['Song_correct'] == "") | (df['Artist_correct'] == "")) else "", axis=1)
    df_all["Artist_correct_search"] = df_all.apply(
        lambda df: df['Search_1'][0] if ((df['Song_correct'] == "") | (df['Artist_correct'] == "")) else "", axis=1)

    # dropping unnecessary columns
    df_all.drop(columns=["Search_1"], inplace=True)

    # cleaning data in columns concerning Song_{number} and Artist_{number}
    column_list = ["Song_correct_search", "Artist_correct_search", ]
    for column in column_list:
        # cleaning row value from words in bracets
        df_all[column] = df_all[column].map(lambda row_value: strippping_bracets_words(row_value))
        # changing row value to lowercase
        df_all[column] = df_all[column].map(lambda row_value: lowercase(row_value))

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\06_ListaPiosenekAPI.xlsx', index=False,
                    encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

def lastfm_search(search_value):
    try:
        length = len(str(search_value))
        API_key = 'e1ff902a157a27deddb5e2d6a76bc5e4'

        if length > 5:
            url = "http://ws.audioscrobbler.com//2.0/?method=track.search&track={value}&api_key={API}&format=json".format(value=search_value, API=API_key)
            search_result = requests.get(url).json()
            print(search_value)
            song = search_result['results']['trackmatches']['track'][0]['name']
            print(song)
            # ['trackmatches']['track']['name']
            artist = search_result['results']['trackmatches']['track'][0]['artist']
            print(artist)
        else:
            artist = ""
            song = ""
    except IndexError:
        artist = ""
        song = ""
    except ValueError:
        artist = ""
        song = ""
    return artist, song


def strippping_bracets_words(row_value):
    pattern1 = re.compile("([(][A-Za-z0-9\W\d_]*\.*[)])")
    pattern2 = re.compile("([\[][A-Za-z0-9\W\d_]*\.*[\]])")
    try:
        if type(pattern1.search(row_value)) == re.Match:
            row_value = row_value.replace(pattern1.search(row_value).group(1), "")
        if type(pattern2.search(row_value)) == re.Match:
            row_value = row_value.replace(pattern2.search(row_value).group(1), "")
        else:
            pass
    except TypeError:
        pass
    return row_value


def lowercase(row_value):
    try:
        row_value = row_value.lower()
    except AttributeError:
        pass
    return row_value

if __name__ == "__main__":
    main()


# Application name	What melody is it - internet crapet
# API key	e1ff902a157a27deddb5e2d6a76bc5e4
# Shared secret	287b60db58af99406d0b0d02fdb62510
# Registered to	sebastiankonicz