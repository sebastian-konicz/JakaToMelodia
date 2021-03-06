import pandas as pd
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# SEARCHING FOR THE CORRECT ARTIST BASED ON KNOWN SONGS
def main():
    # start time of function
    start_time = time.time()

    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\09_ListaPiosenekFuzzy_4.xlsx')

    # getting rid of one entry that distorts future computatuins
    df_all.drop(df_all[df_all["Artist_correct"] == "utah symphony orchestra, the mormon tabernacle choir, frederica von stade, joseph silverstein, utah symphony orchestra, the mormon tabernacle choir and joseph silverstein"].index, inplace=True)

    # replacing NaN values in dataframe
    df_all["Song_correct"].fillna("", inplace=True)
    df_all["Artist_correct"].fillna("", inplace=True)

    # creating new column with concatenated values from song_correct and artist_correct
    df_all["Correct_Concatenated"] = df_all.apply(
        lambda df_all: (str(df_all["Song_correct"]) + " " + str(df_all['Artist_correct'])), axis=1)

    # creating "database" dataframe
    #  databese dataframe - song
    df_correct = df_all[(df_all['Song_correct'] != "") & (df_all['Artist_correct'] != "")].copy(deep=True)
    df_correct.drop(columns=['Song', 'Round', 'Date', 'Month', 'Song_split', 'Artist_split', 'Split_Concatenated'], inplace=True)
    df_correct.drop_duplicates(inplace=True, keep='first')
    # song_dict = pd.Series(df_correct["Song_correct"].values, index=df_correct["Correct_Concatenated"]).to_dict()
    artist_dict = pd.Series(df_correct["Artist_correct"].values, index=df_correct["Correct_Concatenated"]).to_dict()

    # CHECKING SONG - ARTIST WITH FUZZY RATIO
    df_all["Artist_correct_search"] = df_all.apply(
        lambda df_all: fuzzy_ratio(df_all['Song_correct'], artist_dict)
        if (df_all['Artist_correct'] == "") else "", axis=1)

    # coping and pasting correct artist value to artist_corect column
    df_all['Artist_correct'] = df_all.apply(lambda df_all: df_all['Artist_correct_search']
        if (df_all['Artist_correct'] == "") else df_all['Artist_correct'], axis=1)

    # dropping unnecessary column
    df_all.drop(columns=['Artist_correct_search', 'Correct_Concatenated'], inplace=True)

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\10_ListaPiosenekFuzzy_5.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')



# removing key words
def fuzzy_ratio(known_value, dictionary):
    for key, value in dictionary.items():
        searched_value = str(known_value + " " + value)
        ratio = fuzz.token_sort_ratio(key, searched_value)
        if ratio > 95:
            print(searched_value)
            print(key)
            print(ratio)
            result = value
            return result
        else:
            pass

if __name__ == "__main__":
    main()


