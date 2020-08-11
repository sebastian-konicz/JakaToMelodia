import pandas as pd
import time
import re
import requests

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\08_ListaPiosenekFuzzy_3.xlsx')

    # replacing NaN values in dataframe
    df_all["Song_correct"].fillna("", inplace=True)
    df_all["Artist_correct"].fillna("", inplace=True)

    # running search on dataframe
    df_all["Search_1"] = df_all.apply(
        lambda df: deezer_search(df['Split_Concatenated']) if ((df['Song_correct'] == "") & (df['Artist_correct'] == "")) else "", axis=1)

    # unpacking tuple form first search
    df_all["Song_1"] = df_all.apply(
        lambda df: df['Search_1'][1] if ((df['Song_correct'] == "") & (df['Artist_correct'] == "")) else "", axis=1)
    df_all["Artist_1"] = df_all.apply(
        lambda df: df['Search_1'][0] if ((df['Song_correct'] == "") & (df['Artist_correct'] == "")) else "", axis=1)

    df_all.drop(columns=["Search_1"], inplace=True)

    # cleaning data in columns concerning Song_{number} and Artist_{number}
    column_list = ["Song_1", "Artist_1", ]
    for column in column_list:
        # cleaning row value from words in bracets
        df_all[column] = df_all[column].map(lambda row_value: strippping_bracets_words(row_value))
        # changing row value to lowercase
        df_all[column] = df_all[column].map(lambda row_value: lowercase(row_value))

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\09_ListaPiosenekApi_2.xlsx', index=False,
                    encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')


def deezer_search(search_value):
    try:
        length = len(str(search_value))
        if length > 5:
            url = "https://api.deezer.com/search?q='{value}'".format(value=search_value)
            search_result = requests.get(url).json()
            song = search_result['data'][0]['title']
            artist = search_result['data'][0]['artist']['name']
            print(search_value)
            print(artist)
            print(song)
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


