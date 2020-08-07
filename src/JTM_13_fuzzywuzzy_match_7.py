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
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\12_ListaPiosenekFuzzy_6.xlsx')

    # replacing NaN values in dataframe
    df_all["Song_correct"].fillna("", inplace=True)
    df_all["Artist_correct"].fillna("", inplace=True)

    # creating new column with concatenated values from song_correct and artist_correct
    df_all["Correct_Concatenated"] = df_all.apply(
        lambda df_all: (str(df_all["Song_correct"]) + " " + str(df_all['Artist_correct'])), axis=1)

    # replacing NaN values in dataframe
    df_all["Correct_Concatenated"].fillna("", inplace=True)

    # CHECKING SONG - ARTIST WITH FUZZY RATIO
    df_all["Song_Artist_ratio"] = df_all.apply(
        lambda df_all: fuzzy_ratio(df_all['Split_Concatenated'], df_all["Correct_Concatenated"]) if df_all["Correct_Concatenated"] != "" else "", axis=1)

    # # dropping unnecessary column
    # df_all.drop(columns=['Song_correct_search', 'Artist_correct_search', 'Correct_Concatenated'], inplace=True)

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\13_ListaPiosenekFuzzy_7.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')


# removing key words
def fuzzy_ratio(value_1, value_2):
    ratio = fuzz.token_sort_ratio(value_1, value_2)
    print(ratio)
    return ratio
if __name__ == "__main__":
    main()


