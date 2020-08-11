import pandas as pd
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# FUNCTION CHECKING PARTIAL RATIO
def main():
    # start time of function
    start_time = time.time()

    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\06_ListaPiosenekAPI.xlsx')

    # replacing NaN values in dataframe
    df_all["Song_correct"].fillna("", inplace=True)
    df_all["Artist_correct"].fillna("", inplace=True)
    df_all["Song_correct_search"].fillna("", inplace=True)
    df_all["Artist_correct_search"].fillna("", inplace=True)

    # getting correct song/ artist values
    df_all["Song_correct"] = df_all.apply(
        lambda df_all: df_all["Song_correct"] if (df_all["Song_correct"] != "") else df_all["Song_correct_search"],
        axis=1)
    df_all["Artist_correct"] = df_all.apply(
        lambda df_all: df_all["Artist_correct"] if (df_all["Artist_correct"] != "") else df_all[
            "Artist_correct_search"], axis=1)

    # droping unnecessary columns
    df_all.drop(columns=['Song_correct_search', 'Artist_correct_search'], inplace=True)

    # CHECKING VALUES IN KNOWN DATABASE
    # creating "database" dataframes
    #  databese dataframe - song
    df_correct_song = df_all[df_all['Song_correct'] != ""].copy(deep=True)
    df_correct_song.drop(columns=['Song', 'Round', 'Date', 'Month', 'Song_split', 'Artist_split',
                                  'Artist_correct', 'Split_Concatenated'], inplace=True)
    df_correct_song.drop_duplicates(inplace=True, keep='first')
    correct_song_list = df_correct_song['Song_correct'].tolist()
    correct_song_list = [x for x in correct_song_list if str(x) != 'nan']
    print(correct_song_list)

    #  databese dataframe - artist
    df_correct_artist = df_all[df_all['Artist_correct'] != ""].copy(deep=True)
    df_correct_artist.drop(columns=['Song', 'Round', 'Date', 'Month', 'Song_split', 'Artist_split',
                                    'Song_correct', 'Split_Concatenated'], inplace=True)
    df_correct_artist.drop_duplicates(inplace=True, keep='first')
    correct_artist_list = df_correct_artist['Artist_correct'].tolist()
    correct_artist_list = [x for x in correct_artist_list if str(x) != 'nan']
    print(correct_artist_list)

    df_all["Song_correct_search"] = ""
    df_all["Artist_correct_search"] = ""

    # CHECKING SONG - ARTIST WITH FUZZU RATIO
    df_all["Song_correct_search"] = df_all.apply(
        lambda df_all: fuzzy_ratio(df_all["Song_split"], correct_song_list)
        if ((df_all['Song_correct'] == "") | (df_all['Artist_correct'] == "")) else "", axis=1)
    df_all["Artist_correct_search"] = df_all.apply(
        lambda df_all: fuzzy_ratio(df_all["Song_split"], correct_artist_list)
        if ((df_all['Song_correct'] == "") | (df_all['Artist_correct'] == "")) else "", axis=1)

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\07_ListaPiosenekFuzzy_2.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

# removing key words
def fuzzy_ratio(checked_value, searched_list):
    checked_value = str(checked_value)
    for search_item in searched_list:
        length = len(checked_value)
        ratio = fuzz.partial_ratio(checked_value, search_item)
        if length > 6 and ratio > 95:
            result = search_item
            return result
        else:
            pass

if __name__ == "__main__":
    main()


