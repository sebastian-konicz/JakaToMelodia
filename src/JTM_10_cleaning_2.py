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
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\09_ListaPiosenekFuzzy_4.xlsx')

    # CLEANINF ROUND COLUMN
    # replacing NaN values in dataframe
    df_all["Round"].fillna("", inplace=True)

    # changing all values in 'Round' column to string
    df_all['Round'] = df_all['Round'].apply(lambda round: str(round))

    # strippirng space ' ' at the begining and end
    df_all['Round_correct'] = df_all['Round'].map(lambda round: strippping_space_b(round))
    df_all['Round_correct'] = df_all['Round'].map(lambda round: strippping_space_e(round))

    # cleaning column "Round" from dashes
    string_dict_1 = {"  ": " ", ":": "", ".": "", "( ": "", " )": "", "(": "", ")": "",
                     "pierwsza": "runda 1", "trzecia r": "runda 3", "FINAŁ": "runda 4",
                     "Koniec": "Piosenka końcowa", "Początek": "Piosenka początkowa"}
    print(string_dict_1)

    for key, value in string_dict_1.items():
        df_all['Round_correct'] = df_all['Round'].map(lambda round: strippping_and_replacing_1(round, key, value))

    # cleaning column "Round" from dashes
    string_dict_2 = {"iv": "4", "iv:": "4", "IV": "4", "IV:": "4",
                     "iii": "3", "iii:": "3", "III": "3", "III:": "3",
                     "ii": "2", "ii:": "2", "II": "2", "II:": "2",
                     "i": "1", "i:": "1", "I": "1", "I:": "1"}
    print(string_dict_2)

    for key, value in string_dict_2.items():
        df_all['Round_correct'] = df_all['Round'].map(lambda round: strippping_and_replacing_1(round, key, value))

    # strippirng space ' ' at the end
    df_all['Round_correct'] = df_all['Round'].map(lambda round: strippping_space_e(round))

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\10_ListaPiosenekAllClean.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

# removing key words
def key_words(song):
    # replacing unnecessary words
    word_list = ["los szcz.", "los szczęścia", "~dalej ", "~ dalej ", "~dalej~ ", "*dalej* ", "?", "????", "...",
                 "złote przeboje ", "złote przeboje", "1. ", "(perły polskiej piosenki)", "perły polskiej piosenki"]
    for word in word_list:
        if song.find(word) != -1:
            song = song.replace(word, "")
        else:
            pass
    # removing all data when certain words occure
    word_list_2 = ["zapowiedź", "zapowiedzi", "iątek", "201", "2007", "2008", "2010", "2011", "2012", "2013", "2014",
                   "…..", "iązanka", "zaproszenie", "zapowiedz", "piosenek"]
    for word in word_list_2:
        if song.find(word) != -1:
            song = ""
        else:
            pass

    return song

# strippirng song values with dash '- , --- '
def strippping_and_replacing_1(round, key, value):
    round = str(round)
    if round.find(key) != -1:
        round_string = round.replace(str(key), str(value), 1)
        return round_string
    else:
        pass

# strippirng space at the begining ' '
def strippping_space_b(round):
    round = str(round)
    if round[0] == " ":
        round_string = round.replace(' ', "", 1)
        return round_string
    else:
        pass

# strippirng space at the end ' '
def strippping_space_e(round):
    round = str(round)
    if round[-1] == " ":
        round_string = round[:-1]
        return round_string
    else:
        pass

if __name__ == "__main__":
    main()


