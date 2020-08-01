import re
import pandas as pd
import deezer
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenekAllClean.xlsx')

    # getting song value
    # df_all['Deezer_Song'] = df_all['Song'].map(lambda song: deezer_search_song(song))

    row_count = len(df_all.index)
    number_of_items = 100
    number_of_intervals = round(row_count / number_of_items)
    print(row_count, number_of_intervals)

    for value in range(70, number_of_intervals + 1):
        if value == 0:
            truncate_before = value * number_of_items
        else:
            truncate_before = value * number_of_items + 1
        truncate_after = value * number_of_items + number_of_items

        # creating partial dataframe
        df_partial = df_all.truncate(before=truncate_before, after=truncate_after)

        # running search on partial dataframe
        df_partial = partial_dataframe_creation(df_partial)

        # saving partial dataframe to excel
        print('saving file')
        df_partial.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\interim\deezer_API\ListaPiosenek_{start}-{end}.xlsx'.format(start=truncate_before, end=truncate_after), index=False, encoding='ISO-8859-1')


    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

def deezer_search(search_value):
    # initiating empty variables
    song = ""
    artist = ""
    try:
        # initiating deezer client
        client = deezer.Client()
        # running appi search
        search_result_1 = client.search(search_value)
        search_result_2 = client.search(search_value)[0]

        # search results
        song = search_result_1[0]
        artist = search_result_2.artist
    except IndexError:
        pass
    except ValueError:
        pass
    print(song, artist)
    return song, artist

def partial_dataframe_creation(df_all):
    result_list = []
    # running search function
    for key, search_value in df_all['Song'].iteritems():
        # search function values
        song, artist = deezer_search(search_value)
        # adding result items to list
        result_list.append([song, artist])

    # creating dataframe
    result_df = pd.DataFrame(result_list)
    # renaming dataframe columns
    if result_df.empty == True:
        pass
    else:
        result_df.columns = ["Deezer_Song", "Deezer_Artist"]

    # reseting index
    df_all.reset_index(drop=True, inplace=True)

    # concatenating dataframes
    df_all = pd.concat([df_all, result_df], axis=1, sort=False)

    return df_all

if __name__ == "__main__":
    main()


