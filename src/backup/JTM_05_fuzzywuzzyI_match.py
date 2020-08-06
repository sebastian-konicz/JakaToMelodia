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
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\04_ListaPiosenekAPIClean.xlsx')

    # CHECKING SONG - ARTIST WITH FUZZU RATIO
    # checking fuzzy ration
    # checking if the "song - artist" placment is inverted
    df_all["Song_split_Artist_1_ratio"] = df_all.apply(lambda df_all: fuzzy_ratio(df_all["Song_split"], df_all["Artist_1"]), axis=1)
    df_all["Artist_split_Song_1_ratio"] = df_all.apply(lambda df_all: fuzzy_ratio(df_all["Artist_split"], df_all["Song_1"]), axis=1)

    # checking if the "song - artist" placment is correct
    df_all["Artist_split_Artist2_ratio"] = df_all.apply(lambda df_all: fuzzy_ratio(df_all["Artist_split"], df_all["Artist_2"]), axis=1)
    df_all["Song_split_Song_2_ratio"] = df_all.apply(lambda df_all: fuzzy_ratio(df_all["Song_split"], df_all["Song_2"]), axis=1)

    # creating column with correct song and artist
    df_all['Song_correct'] = df_all.apply(lambda df_all: df_all["Song_1"] if ((df_all['Song_split_Artist_1_ratio'] >= 80) & (df_all['Artist_split_Song_1_ratio'] >= 80)) else "", axis=1)
    df_all['Artist_correct'] = df_all.apply(lambda df_all: df_all["Artist_1"] if ((df_all['Song_split_Artist_1_ratio'] >= 80) & (df_all['Artist_split_Song_1_ratio'] >= 80)) else "", axis=1)

    # getting rid of unnecessary columns
    df_all.drop(columns=['Artist_1', 'Song_1', 'Artist_2', 'Song_2',
                         'Song_split_Artist_1_ratio', 'Artist_split_Song_1_ratio',
                         'Artist_split_Artist2_ratio',	'Song_split_Song_2_ratio'], inplace=True)

    # CHECKING VALUES IN KNOWN DATABASE
    # creating "database" dataframes
    #  databese dataframe - song
    df_correct_song = df_all[df_all['Song_correct'] != ""].copy(deep=True)
    df_correct_song.drop(columns=['Song', 'Round', 'Date', 'Month', 'Song_split', 'Artist_split', 'Artist_correct'], inplace=True)
    df_correct_song.drop_duplicates(inplace=True, keep='first')
    correct_song_list = df_correct_song['Song_correct'].tolist()
    print(correct_song_list)

    #  databese dataframe - artist
    df_correct_artist = df_all[df_all['Artist_correct'] != ""].copy(deep=True)
    df_correct_artist.drop(columns=['Song', 'Round', 'Date', 'Month', 'Song_split', 'Artist_split', 'Song_correct'], inplace=True)
    df_correct_artist.drop_duplicates(inplace=True, keep='first')
    correct_artist_list = df_correct_artist['Artist_correct'].tolist()
    print(correct_artist_list)

    # updatdating song correct and artist correct with similar values found in dataframe
    # searching for correct artist names in "Song_split" column

    df_all['Song_correct_search'] = ""
    df_all['Artist_correct_search'] = ""

    for artist in correct_artist_list:
        print(artist)
        df_all['Artist_correct_search'] = df_all.apply(
            lambda df_all: artist if (df_all["Song_split"] == artist) else df_all['Artist_correct_search'], axis=1)
        df_all['Artist_correct_search'] = df_all.apply(
            lambda df_all: artist if (df_all["Artist_split"] == artist) else df_all['Artist_correct_search'], axis=1)

    print('saving file - artist')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\05_ListaPiosenekFuzzy-artist.xlsx', index=False,
                    encoding='ISO-8859-1')

    for song in correct_song_list:
        print(song)
        df_all['Song_correct_search'] = df_all.apply(
            lambda df_all: song if (df_all["Song_split"] == song) else df_all['Song_correct_search'], axis=1)
        df_all['Song_correct_search'] = df_all.apply(
            lambda df_all: song if (df_all["Artist_split"] == song) else df_all['Song_correct_search'], axis=1)

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\05_ListaPiosenekFuzzy.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

# removing key words
def fuzzy_ratio(value1, value2):
    try:
        result = fuzz.token_sort_ratio(value1, value2)
    except AttributeError:
        pass
    return result

# removing key words
def search_correct_song(search_value, correct_artist_list):
    for correct_artist in correct_artist_list:
        print(search_value + " + " + correct_artist)
        if search_value == correct_artist:
            search_value = correct_artist
        else:
            search_value = ""
    return search_value

if __name__ == "__main__":
    main()


