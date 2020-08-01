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
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenekAPIClean.xlsx')


    # creating deezer cleen columns
    df_all["Song_Song_ratio"] = df_all.apply(lambda df_all: fuzzy_ratio(df_all["Song_split"], df_all["Deezer_Song_clean"]), axis=1)
    df_all["Song_Artist_ratio"] = df_all.apply(lambda df_all: fuzzy_ratio(df_all["Artist_split"], df_all["Deezer_Song_clean"]), axis=1)
    df_all["Artist_Song_ratio"] = df_all.apply(lambda df_all: fuzzy_ratio(df_all["Song_split"], df_all["Deezer_Artist_clean"]), axis=1)
    df_all["Artist_Artist_ratio"] = df_all.apply(lambda df_all: fuzzy_ratio(df_all["Artist_split"], df_all["Deezer_Artist_clean"]), axis=1)

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenekFuzzy.xlsx', index=False, encoding='ISO-8859-1')

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

if __name__ == "__main__":
    main()


