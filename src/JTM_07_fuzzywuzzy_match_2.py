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
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\06_ListaPiosenekAPI.xlsx')

    # Getting rid of to long song names / artist names
    df_all["Song_correct_search"] = df_all["Song_correct_search"].apply(
        lambda df_all: df_all if (len(str(df_all)) <= 50) else "")
    df_all["Artist_correct_search"] = df_all["Artist_correct_search"].apply(
        lambda df_all: df_all if (len(str(df_all)) <= 50) else "")

    # replacing NaN values in dataframe
    df_all["Song_correct"].fillna("", inplace=True)
    df_all["Artist_correct"].fillna("", inplace=True)
    df_all["Song_correct_search"].fillna("", inplace=True)
    df_all["Artist_correct_search"].fillna("", inplace=True)

    # creating new column with concatenated values from song_correct_search and artist_correct_search
    df_all["Search_Concatenated"] = df_all.apply(
        lambda df_all: (str(df_all["Song_correct_search"]) + " " + str(df_all['Artist_correct_search']))
        if (df_all['Song_correct_search'] != "") & (df_all['Artist_correct_search'] != "") else "", axis=1)

    # replacing NaN values in dataframe
    df_all["Search_Concatenated"].fillna("", inplace=True)

    # Checking fuzzy ratio of Search_Concatenated and Split_Concatenated column
    df_all["Search_Concatenated"] = df_all.apply(
        lambda df_all: fuzzy_ratio(df_all['Split_Concatenated'], df_all['Search_Concatenated'])
        if (df_all['Search_Concatenated'] != "") else "", axis=1)

    # replacing NaN values in dataframe
    df_all["Search_Concatenated"].fillna("", inplace=True)

    # updatdating song correct and artist correct with correct values form API search
    df_all["Song_correct"] = df_all.apply(
        lambda df_all: df_all['Song_correct_search'] if ((df_all['Song_correct'] == "") & (df_all["Search_Concatenated"] != "")) else df_all['Song_correct'], axis=1)

    df_all["Artist_correct"] = df_all.apply(
        lambda df_all: df_all['Artist_correct_search'] if ((df_all['Artist_correct'] == "") & (df_all["Search_Concatenated"] != "")) else df_all['Artist_correct'], axis=1)

    # droping unnecessary columns
    df_all.drop(columns=['Song_correct_search', 'Artist_correct_search', 'Search_Concatenated'], inplace=True)

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\07_ListaPiosenekFuzzy_2.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')


def fuzzy_ratio(split_value, search_value):
    ratio = fuzz.token_sort_ratio(split_value, search_value)
    if ratio > 95:
        print(split_value)
        print(search_value)
        print(ratio)
        result = search_value
        return result
    else:
        pass

if __name__ == "__main__":
    main()


