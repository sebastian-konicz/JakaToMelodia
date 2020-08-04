import pandas as pd
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\08_ListaPiosenekApi_2.xlsx')

    # replacing NaN values in dataframe
    df_all["Song_1"].fillna("", inplace=True)
    df_all["Artist_1"].fillna("", inplace=True)

    # creating new column with concatenated values from song_correct and artist_correct
    df_all["Search_Concatenated"] = df_all.apply(
        lambda df_all: (str(df_all['Song_1']) + " " + str(df_all['Artist_1'])), axis=1)

    # creating "database" dataframes
    #  databese dataframe - song
    df_correct = df_all[df_all['Search_Concatenated'] != ""].copy(deep=True)
    df_correct.drop(columns=['Song', 'Round', 'Date', 'Month', 'Song_split', 'Artist_split',
                             'Song_correct', 'Artist_correct', 'Split_Concatenated', 'Correct_Concatenated'], inplace=True)
    df_correct.drop_duplicates(inplace=True, keep='first')
    song_dict = pd.Series(df_correct["Song_1"].values, index=df_correct["Search_Concatenated"]).to_dict()
    artist_dict = pd.Series(df_correct["Artist_1"].values, index=df_correct["Search_Concatenated"]).to_dict()

    # CHECKING SONG - ARTIST WITH FUZZU RATIO
    df_all["Song_correct_search"] = df_all.apply(
        lambda df_all: fuzzy_ratio(df_all['Split_Concatenated'], song_dict) if (df_all['Split_Concatenated'] != "") else "", axis=1)
    df_all["Artist_correct_search"] = df_all.apply(
        lambda df_all: fuzzy_ratio(df_all['Split_Concatenated'], artist_dict) if (df_all['Split_Concatenated'] != "") else "", axis=1)

    # Creating new column song/artist_correct_sum with all correct song artist value
    df_all['Song_correct_sum'] = df_all.apply(
        lambda df_all: match_condition(df_all["Song_correct"], df_all['Song_1']), axis=1)
    df_all['Artist_correct_sum'] = df_all.apply(
        lambda df_all: match_condition(df_all["Artist_correct"], df_all['Artist_1']), axis=1)

    # cleaning dataframe from unnecessary columns
    df_all['Song_correct'] = df_all['Song_correct_sum']
    df_all['Artist_correct'] = df_all['Artist_correct_sum']
    df_all.drop(columns=['Correct_Concatenated', 'Song_1', 'Artist_1', 'Search_Concatenated',
                         'Song_correct_search', 'Artist_correct_search', 'Song_correct_sum', 'Artist_correct_sum'],
                inplace=True)

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\09_ListaPiosenekFuzzy_4.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

# removing key words
def match_condition(value_1, value_2):
        value_1_len = len(str(value_1))
        value_2_len = len(str(value_2))
        if (value_1_len > value_2_len):
            result = value_1
        elif (value_1_len < value_2_len):
            result = value_2
        # elif ((value_1 != " ") & (value_2 != " ")):
        #     result = "warunek 3"
        else:
            result = value_1
        return result

# removing key words
def fuzzy_ratio(checked_value, dictionary):

    for key, value in dictionary.items():
        ratio = fuzz.token_sort_ratio(checked_value, key)
        if ratio > 85:
            print(ratio)
            print(checked_value)
            print(key)
            print(value)
            result = value
            return result
        else:
            pass

if __name__ == "__main__":
    main()


