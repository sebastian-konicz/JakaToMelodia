import re
import pandas as pd
import deezer

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenekAllCleanShort.xlsx')

    # initiating a client
    client = deezer.Client()

    # getting Artist value
    df_all['Artist_Deezer'] = df_all['Artist_split'].map(lambda artist: deezer_artist(artist))

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenekAllDeezer.xlsx', index=False, encoding='ISO-8859-1')

# artist search
def deezer_artist(artist):
    try:
        client = deezer.Client()
        artist = client.search(artist, relation='artist')
        artist = [artist[0]]
        print(artist)
    except IndexError:
        pass
    return artist

if __name__ == "__main__":
    main()


