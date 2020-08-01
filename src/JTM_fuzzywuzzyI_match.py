import re
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenekAllClean.xlsx')

    row_count = len(df_all.index)
    number_of_items = 100
    number_of_intervals = 190

    df_all = []
    for value in range(0, number_of_intervals + 1):
        if value == 0:
            start_number = value * number_of_items
        else:
            start_number = value * number_of_items + 1
        end_number = value * number_of_items + number_of_items

        # loading partial file
        df_partial = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\interim\deezer_API\ListaPiosenek_{start}-{end}.xlsx'.format(start=start_number, end=end_number))

        # adding partial file to list
        df_all.append(df_partial)

    df_all = pd.concat(df_all, axis=0, sort=False)

    print(df_all)

    # CLEANINF SONG COLUMN
    # removing key words
    dict = {"Deezer_Song": "<Track: ", "Deezer_Artist": "<Artist: ", "Deezer_Album": "<Album: "}
    for key, value in dict.items():
        df_all[key] = df_all[key].map(lambda row_value: key_words(row_value, value))

    # creating deezer cleen columns
    df_all["Deezer_Song_clean"] = df_all["Deezer_Song"].map(lambda row_value: strippping_bracets_words(row_value))
    df_all["Deezer_Artist_clean"] = df_all["Deezer_Artist"].map(lambda row_value: strippping_bracets_words(row_value))

    # changing values in colum to lower case
    df_all["Deezer_Song_clean"] = df_all["Deezer_Song_clean"].map(lambda row_value: lowercase(row_value))
    df_all["Deezer_Artist_clean"] = df_all["Deezer_Artist_clean"].map(lambda row_value: lowercase(row_value))

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenekAPIClean.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

# removing key words
def key_words(row_value, value):
    # replacing unnecessary words
    word_list = [value, ">"]
    try:
        for word in word_list:
            if row_value.find(word) != -1:
                row_value = row_value.replace(word, "")
            else:
                pass
    except AttributeError:
        pass
    return row_value

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


