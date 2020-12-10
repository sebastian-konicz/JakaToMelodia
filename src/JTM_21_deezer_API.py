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
    print('Loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\interim\Lista_piosenek_youtube.xlsx')

    # running search on dataframe
    df_all["Search"] = df_all.apply(lambda df: deezer_search(df['Song'], df['Artist']), axis=1)

    # unpacking tuple form first search
    df_all["Artist_deezer"] = df_all['Search'].apply(lambda df: df[0])
    df_all["Song_deezer"] = df_all['Search'].apply(lambda df: df[1])
    df_all["Song_id_deezer"] = df_all['Search'].apply(lambda df: df[2])

    # id_list = df_all["Song_id_deezer"].tolist()
    # print(id_list)
    #
    # access_token = 'frHIJyJWLxQcxKsJbUYyzvlJVAIJqGpd4RaiQM2Wef3O8qdfM51'
    # playlist_id = 1703463421
    #
    # for id in id_list:
    #     url = 'http://api.deezer.com/playlist/{playlist_id}>/tracks?access_token={access_token}&request_method=post&songs={track_id}'.format(playlist_id=playlist_id, access_token=access_token, track_id=id)
    #     search_result = requests.get(url).json()
    #     print(search_result)

    # saving partial dataframe to excel
    print('Saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\interim\Lista_piosenek_deezer.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

def deezer_search(song, artist):
    try:
        url = "https://api.deezer.com/search?q='{value1}' '{value2}'".format(value1=song, value2=artist)
        search_result = requests.get(url).json()
        position = looping_api_rank(search_result)
        song = search_result['data'][position]['title']
        artist = search_result['data'][position]['artist']['name']
        id = search_result['data'][position]['id']
        print(artist, song, id)
    except IndexError:
        artist = ""
        song = ""
        id = ""
    except ValueError:
        artist = ""
        song = ""
        id = ""
    return artist, song, id

# getting the song with the highest deezer rank
def looping_api_rank(search_result):
    search_no = []
    song_rank = []
    search_total = search_result['total']
    if int(search_total) < 25:
        search_total = search_total
    else:
        search_total = 25
    for search_number in range(search_total):
       search_no.append(search_number)
       song_rank.append(search_result['data'][search_number]['rank'])
    rank_dict = dict(zip(search_no, song_rank))
    position = max(rank_dict, key=rank_dict.get)
    return position

if __name__ == "__main__":
    main()


