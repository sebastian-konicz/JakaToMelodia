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
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\02_ListaPiosenekAllClean.xlsx')

    # getting song value
    # df_all['Deezer_Song'] = df_all['Song'].map(lambda song: deezer_search_song(song))

    row_count = len(df_all.index)
    number_of_items = 500
    number_of_intervals = round(row_count / number_of_items)
    print(row_count, number_of_intervals)

    for value in range(0, number_of_intervals + 1):
        if value == 0:
            truncate_before = value * number_of_items
        else:
            truncate_before = value * number_of_items + 1
        truncate_after = value * number_of_items + number_of_items

        # creating partial dataframe
        df_partial = df_all.truncate(before=truncate_before, after=truncate_after)

        # running search on partial dataframe
        # search with the assumption that in df['Song_split') is the artist value
        df_partial["Search_1"] = df_partial.apply(lambda df: deezer_search(df['Song_split'], df['Artist_split']), axis=1)
        # search with the assumption that in df['artist_split') is the artist value
        df_partial["Search_2"] = df_partial.apply(lambda df: deezer_search(df['Artist_split'], df['Song_split']), axis=1)

        # unpacking tuple form first search
        df_partial["Artist_1"] = df_partial['Search_1'].apply(lambda df: df[0])
        df_partial["Song_1"] = df_partial['Search_1'].apply(lambda df: df[1])

        # unpacking tuple form first search
        df_partial["Artist_2"] = df_partial['Search_2'].apply(lambda df: df[1])
        df_partial["Song_2"] = df_partial['Search_2'].apply(lambda df: df[0])

        df_partial.drop(columns=["Search_1", "Search_2"], inplace=True)

        # cleaning data in columns concerning Song_{number} and Artist_{number}
        column_list = ["Artist_1", "Song_1", "Artist_2", "Song_2"]
        for column in column_list:
            # cleaning row value from words in bracets
            df_partial[column] = df_partial[column].map(lambda row_value: strippping_bracets_words(row_value))
            # changing row value to lowercase
            df_partial[column] = df_partial[column].map(lambda row_value: lowercase(row_value))

        # saving partial dataframe to excel
        print('saving file')
        df_partial.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\interim\deezer_API\03_ListaPiosenek_{start}-{end}.xlsx'.format(start=truncate_before, end=truncate_after), index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

def deezer_search(search_value_1, search_value_2):
    try:
        url = "https://api.deezer.com/search?q=artist:'{value1}' track:'{value2}'".format(value1=search_value_1, value2=search_value_2)
        search_result = requests.get(url).json()
        song = search_result['data'][0]['title']
        artist = search_result['data'][0]['artist']['name']
        print(artist)
        print(song)
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


