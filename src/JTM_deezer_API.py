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
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenekAllCleanShort.xlsx')

    # getting song value
    # df_all['Deezer_Song'] = df_all['Song'].map(lambda song: deezer_search_song(song))


    result_list = []

    # running search function
    for key, search_value in df_all['Song'].iteritems():
        print(search_value)
        # search function values
        song, artist, album, link, preview = deezer_search(search_value)
        # adding result items to list
        result_list.append([song, artist, album, link, preview])

    # creating dataframe
    result_df = pd.DataFrame(result_list)
    # renaming dataframe columns
    print(result_df)
    if result_df.empty == True:
        pass
    else:
        result_df.columns = ["Deezer_Song", "Deezer_Artist", "Deezer_Album", "Deezer_Link", "Deezer_Preview"]

    # concatenating dataframes
    df_all = pd.concat([df_all, result_df], axis=1, sort=False)

    print(df_all)

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenekAllDeezer.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

def deezer_search(search_value):
    # initiating empty variables
    song = ""
    artist = ""
    album = ""
    link = ""
    preview = ""
    try:
        # initiating deezer client
        client = deezer.Client()
        # running appi search
        search_result_1 = client.search(search_value)
        search_result_2 = client.search(search_value)[0]

        # search results
        song = search_result_1[0]
        artist = search_result_2.artist
        album = search_result_2.album
        link = search_result_2.link
        preview = search_result_2.preview
    except IndexError:
        pass
    except ValueError:
        pass
    print(song, artist, album, link, preview)
    return song, artist, album, link, preview


        # getting artist value
    # df_all['Deezer_Artist_'] = df_all['Song'].map(lambda song: deezer_search_artist(song))

    # # getting deezer preview
    # df_all['Deezer_Album'] = df_all['Song'].map(lambda song: deezer_search_album(song))
    #
    # # getting deezer link
    # df_all['Deezer_Link'] = df_all['Song'].map(lambda song: deezer_search_link(song))
    #
    # # getting deezer preview
    # df_all['Deezer_Preview'] = df_all['Song'].map(lambda song: deezer_search_preview(song))

# def deezer_search_song(song):
#     try:
#         print(song)
#         client = deezer.Client()
#         song = client.search(song)
#         song = song[0]
#         print(song)
#     except IndexError:
#         pass
#     except ValueError:
#         pass
#     return song
#
# def deezer_search_artist(song):
#     artist = ""
#     try:
#         print(song)
#         client = deezer.Client()
#         song = client.search(song)[0]
#         performer = song.artist
#         print(artist)
#     except IndexError:
#         pass
#     except ValueError:
#         pass
#     return artist
#
# def deezer_search_album(song):
#     album = ""
#     try:
#         print(song)
#         client = deezer.Client()
#         song = client.search(song)[0]
#         album = song.album
#         print(album)
#     except IndexError:
#         pass
#     except ValueError:
#         pass
#     return album
#
# def deezer_search_link(song):
#     link = ""
#     try:
#         print(song)
#         client = deezer.Client()
#         song = client.search(song)[0]
#         link = song.link
#         print(link)
#     except IndexError:
#         pass
#     except ValueError:
#         pass
#     return link
#
# def deezer_search_preview(song):
#     preview = ""
#     try:
#         print(song)
#         client = deezer.Client()
#         song = client.search(song)[0]
#         preview = song.preview
#         print(preview)
#     except IndexError:
#         pass
#     except ValueError:
#         pass
#     return preview

if __name__ == "__main__":
    main()


