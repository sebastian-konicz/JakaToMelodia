import re
import pandas as pd
import re
import time
from datetime import datetime

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
    df_all['Round'] = df_all['Round'].map(lambda round: strippping_space_b(round))
    df_all['Round'] = df_all['Round'].map(lambda round: strippping_space_e(round))

    # cleaning column "Round" from dashes
    string_dict_1 = {"pierwsza": "runda 1", "trzecia r": "runda 3", "FINAŁ": "runda 4", "[color=ye": "runda 1",
                     "runda dod": "runda d", "dodatkowa": "runda d", "druga run": "runda 2", "4. dynami": "runda 4",
                     "Początek": "start", "Koniec": "end"}

    for key, value in string_dict_1.items():
        df_all['Round'] = df_all['Round'].map(lambda round: strippping_and_replacing_1(round, key, value))

    # cleaning column "Round" from dashes
    string_dict_2 = {"  ": " ", ":": "", ".": "", "( ": "", " )": "", "(": "", ")": "",
                     " [": "", " ]": "", " -": "", " –": "",
                     "iv": "4", "iv:": "4", "IV": "4", "IV:": "4",  "lV": "4",
                     "iii": "3", "iii:": "3", "III": "3", "III:": "3", "lll": "3",
                     "ii": "2", "ii:": "2", "II": "2", "II:": "2",  "ll": "2",
                     "i": "1", "i:": "1", "I": "1", "I:": "1", "l": "1"}

    for key, value in string_dict_2.items():
        df_all['Round'] = df_all['Round'].map(lambda round: strippping_and_replacing_1(round, key, value))

    # changing the order for example from "1 runda" to "runda 1"
    string_dict_3 = {"1 runda": "runda 1", "2 runda": "runda 2", "3 runda": "runda 3", "4 runda": "runda 4", "  ": " "}

    for key, value in string_dict_3.items():
        df_all['Round'] = df_all['Round'].map(lambda round: strippping_and_replacing_1(round, key, value))

    # Stripping string to be 7 characters long
    df_all['Round'] = df_all['Round'].map(lambda round: round[:7])

    # CLEANINF DATE COLUMN
    # replacing NaN values in dataframe
    df_all["Date"].fillna("", inplace=True)

    # changing all values in 'Round' column to string
    df_all['Date'] = df_all['Date'].apply(lambda date: str(date))

    # splitting values in Song accordingly to "."
    # new data frame with split value columns
    split_df = df_all["Date"].apply(lambda value: re.split("[.]", value))

    # creating a datafrmae and setting new column names
    split_df = pd.DataFrame(split_df.to_list(), columns=['Day', 'Month_2', 'Year'])

    # changing day column to correct values
    split_df['Day'] = split_df['Day'].map(lambda day: "0" + str(day) if len(str(day)) == 1 else day)

    # changing year column to correct values
    string_dict_4 = {"20079": "2007", "1012": "2012"}

    for key, value in string_dict_4.items():
        split_df['Year'] = split_df['Year'].map(lambda year: strippping_and_replacing_1(year, key, value))

    string_dict_5 = {"201": "2011", "2": "2010", "07": "2007", "08": "2008", "09": "2009",
                     "10": "2010", "11": "2011", "12": "2012", "13": "2013", "14": "2014", "15": "2015",
                     "16": "2016", "17": "2017", "18": "2018"}

    for key, value in string_dict_5.items():
        split_df['Year'] = split_df['Year'].map(lambda year: changing_values(year, key, value))

    # getting rid of empty values
    column_list = ['Day', 'Month_2', 'Year']
    for column_name in column_list:
       split_df[column_name] = split_df[column_name].apply(lambda df: "" if df is None else df)

    # creating new column with correct date
    split_df['Date_amended'] = split_df.apply(
        lambda df: df['Year'] +"-"+ df['Month_2'] +"-"+df['Day']
        if (df['Year'] != "") & (df['Month_2'] != "") & (df['Day'] != "")
        else "", axis=1)

    # # converting column to datetime
    # split_df['Date_amended'] = split_df['Date_amended'].apply(lambda df: datetime.strptime(df, "%d %B, %Y"))

    # getting ridd of unnecessary columns
    split_df.drop(columns=['Day', 'Month_2', 'Year'], inplace=True)

    # concatenating dataframes
    df_all = pd.concat([df_all, split_df], axis=1, sort=False)

    # CLEANINF MONTH COLUMN AND CHANGIN IT TO TYPE OF EPISODE (NORMAL/SPECIAL
    # replacing NaN values in dataframe
    df_all['Month'].fillna("", inplace=True)
    df_all['Month_amended'] = df_all['Month'].map(
        lambda month: "Specjalny"
        if (month.find("Specjalne") != -1) | (month.find("specjalne") != -1) | (month.find("SPECJALNE") != -1)
        else "Normalny")

    df_all['Episode_type'] = df_all['Month_amended']
    df_all['Date'] = split_df['Date_amended']

    # getting ridd of unnecessary columns
    df_all.drop(columns=['Month_amended', 'Date_amended', 'Song'], inplace=True)

    df_all = df_all[['Song_correct', 'Artist_correct', 'Split_Concatenated', 'Song_split', 'Artist_split', 'Round', 'Date', 'Episode_type']]

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\10_ListaPiosenekAllClean.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

# strippirng song values with dash '- , --- '
def strippping_and_replacing_1(round, key, value):
    round = str(round)
    if round.find(key) != -1:
        round = round.replace(str(key), str(value), 1)
    else:
        pass
    return round

def changing_values(changed_value, key, value):
    changed_value = str(changed_value)
    if (changed_value.find(key) != -1) and (len(str(changed_value)) <= 3):
        changed_value = changed_value.replace(str(key), str(value), 1)
    else:
        pass
    return changed_value

# strippirng space at the begining ' '
def strippping_space_b(round):
    try:
        if round[0] == " ":
            song = round.replace(' ', "", 1)
        else:
            pass

    except IndexError:
        pass
    except TypeError:
        pass
    return round

# strippirng space at the end ' '
def strippping_space_e(round):
    try:
        if round[-1] == " ":
            round = round[:-1]
        else:
            pass

    except IndexError:
        pass
    return round

if __name__ == "__main__":
    main()


