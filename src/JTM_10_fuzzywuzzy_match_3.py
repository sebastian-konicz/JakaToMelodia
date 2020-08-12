import pandas as pd
import time
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
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\08_ListaPiosenekFuzzy_3.xlsx')

    # replacing NaN values in dataframe
    df_all["Song_correct"].fillna("", inplace=True)
    df_all["Artist_correct"].fillna("", inplace=True)

    # creating new column with concatenated values from song_correct and artist_correct
    df_all["Correct_Concatenated"] = df_all.apply(
        lambda df_all: (str(df_all["Song_correct"]) + " " + str(df_all['Artist_correct'])), axis=1)

    # replacing NaN values in dataframe
    df_all["Correct_Concatenated"].fillna("", inplace=True)

    # creating "database" dataframe
    #  databese dataframe - song
    df_correct = df_all[(df_all['Song_correct'] != "") & (df_all['Artist_correct'] != "")].copy(deep=True)
    df_correct.drop(columns=['Song', 'Round', 'Date', 'Month', 'Song_split', 'Artist_split', 'Split_Concatenated'], inplace=True)
    df_correct.drop_duplicates(inplace=True, keep='first')
    song_list = pd.Series(df_correct["Song_correct"]).tolist()
    artist_list = pd.Series(df_correct["Artist_correct"]).tolist()
    print(song_list)
    print(artist_list)

    # CHECKING SONG - ARTIST WITH FUZZY RATIO
    df_all["Song_correct_search"] = df_all.apply(
        lambda df_all: fuzzy_ratio_song(df_all['Split_Concatenated'], song_list)
        if ((df_all['Song_correct'] == "") & (df_all['Artist_correct'] == "")) else "", axis=1)
    df_all["Artist_correct_search"] = df_all.apply(
        lambda df_all: fuzzy_ratio_artist(df_all['Split_Concatenated'], artist_list)
        if ((df_all['Song_correct'] == "") & (df_all['Artist_correct'] == "")) else "", axis=1)

    # # coping and pasting correct song/artist value to song/artist_corect column
    # df_all['Song_correct'] = df_all.apply(lambda df_all: df_all['Song_correct_search']
    #     if (df_all['Song_correct'] == "") else df_all['Song_correct'], axis=1)
    # df_all['Artist_correct'] = df_all.apply(lambda df_all: df_all['Artist_correct_search']
    #     if (df_all['Artist_correct'] == "") else df_all['Artist_correct'], axis=1)
    #
    # # dropping unnecessary column
    # df_all.drop(columns=['Song_correct_search', 'Artist_correct_search', 'Correct_Concatenated'], inplace=True)

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\09_ListaPiosenekFuzzy_4-Copy.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

# removing key words
def fuzzy_ratio_song(split, list):
    highest = process.extractOne(split, list)
    ratio = highest[1]
    value = highest[0]
    if ratio >= 90:
        print(ratio)
        print(split)
        print(value)
        return value
    else:
        pass

def fuzzy_ratio_artist(split, list):
    highest = process.extractOne(split, list)
    ratio = highest[1]
    value = highest[0]
    if (len(str(value)) > 3) & (ratio >= 95):
        print(ratio)
        print(split)
        print(value)
        print(len(str(value)))
        return value
    else:
        pass

if __name__ == "__main__":
    main()


