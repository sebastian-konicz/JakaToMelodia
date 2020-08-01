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
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenekAll.xlsx')

    # CLEANINF SONG COLUMN
    # removing key words
    df_all['Song'] = df_all['Song'].map(lambda song: key_words(song))

    # strippirng song values with underscore '_'
    df_all['Song'] = df_all['Song'].map(lambda song: strippping_underscore(song))

    # strippirng song values with two slashes '//'
    df_all['Song'] = df_all['Song'].map(lambda song: strippping_slashes(song))

    # replacing diffrent dashes'-'
    df_all['Song'] = df_all['Song'].map(lambda song: strippping_dahes_1(song))

    # strippirng song values with dash '- , --- '
    df_all['Song'] = df_all['Song'].map(lambda song: strippping_dahes_2(song))

    # strippirng song values with words between bracets '(word)'
    df_all['Song'] = df_all['Song'].map(lambda song: strippping_bracets_words(song))

    # removing certain characters
    df_all['Song'] = df_all['Song'].map(lambda song: strippping_characters(song))

    # strippirng song values with apostrophe '"'
    df_all['Song'] = df_all['Song'].map(lambda song: strippping_apostrophe(song))

    # strippirng song values with dash '- , --- '
    df_all['Song'] = df_all['Song'].map(lambda song: strippping_dahes_2(song))

    # strippirng space at the begining ' '
    df_all['Song'] = df_all['Song'].map(lambda song: strippping_space(song))

    # dropping empty rows
    df_all.drop(df_all[df_all['Song'] == ""].index, inplace=True)

    # reseting index
    df_all.reset_index(drop=True, inplace=True)

    # Splitting values in Song accordingly to "-"
    # new data frame with split value columns
    split_df = df_all["Song"].apply(lambda value: re.split("(-)", value, maxsplit=1))

    # creating a datafrmae and setting new column names
    split_df = pd.DataFrame(split_df.to_list(), columns=['Song_split', '-', 'Artist_split'])

    # concatenating dataframes
    df_all = pd.concat([df_all, split_df], axis=1, sort=False)

    # dropping unnecessary column ["-"]
    df_all.drop(columns=["-"], inplace=True)

    # CLEANING CONCATENATED DATAFRAME
    # cleaning column "Song_split" from tailing white space
    df_all['Song_split'] = df_all['Song_split'].map(lambda song: strippping_space_e(song))

    # cleaning column "Artist_split" from dashes
    df_all['Artist_split'] = df_all['Artist_split'].map(lambda artist: strippping_dahes_2(artist))

    # cleaning column "Artist_split" from space at the begining ' '
    df_all['Artist_split'] = df_all['Artist_split'].map(lambda artist: strippping_space(artist))

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenekAllClean.xlsx', index=False, encoding='ISO-8859-1')

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

# strippirng song values with underscore '_'
def strippping_underscore(song):
    if song.find("_") != -1:
        index = song.find("_")
        song = song[: index]
    else:
        pass
    return song

# strippirng song values with two slashes '//'
def strippping_slashes(song):
    if song.find("//") != -1:
        index = song.find("//")
        song = song[: index]
    else:
        pass
    return song

# replacing diffrent dashes'-'
def strippping_dahes_1(song):
    characterlist = ['\u002D', '\u058A', '\u05BE', '\u1400', '\u1806', '\u2010-', '\u2015', '\u2E17', '\u2E1A', '\u2E3A',
                     '\u2E3B', '\u2E40', '\u301C', '\u3030', '\u30A0', '\uFE31', '\uFE32', '\uFE58', '\uFE63', '\uFF0D',
                     '\u2212', '\u2013']
    for value in characterlist:
        pattern1 = re.compile(value)
        if type(pattern1.search(song)) == re.Match:
            song = song.replace(pattern1.search(song).group(0), "-")
        else:
            pass
    if song.find(chr(45)) != -1:
        song = song.replace(chr(45), "-")
    if song.find(chr(8211)) != -1:
        song = song.replace(chr(150), "-")
    else:
        pass
    return song

# strippirng song values with dash '- , --- '
def strippping_dahes_2(song):
    try:
        if song.find("(-)") != -1:
            song = song.replace("(-)", "")
        if song.find("---") != -1:
            song = song.replace("---", "")
        if song.find("-   -") != -1:
            song = song.replace("-   -", "")
        if song.find("-  -") != -1:
            song = song.replace("-  -", "")
        if song.find("-") == 0:
            song = song[1:]
        if song.find("-") == 1:
            song = song[2:]
        if song.find("-") == 2:
            song = song[3:]
        if song.find("-") == 3:
            song = song[4:]
        else:
            pass
    except AttributeError:
        pass
    return song

# strippirng song values with words between bracets '(word)'
def strippping_bracets_words(song):
    pattern1 = re.compile("([(][A-Za-z]*[\W\d_]*[0-9]*\.*[)])")
    pattern2 = re.compile("([(]\s*[a-z]\.*[)])")

    if type(pattern1.search(song)) == re.Match:
        song = song.replace(pattern1.search(song).group(1), "")
    if type(pattern2.search(song)) == re.Match:
        song = song.replace(pattern2.search(song).group(1), "")
    else:
        pass

    try:
        if song[-1] == ')' and song.find("(") != -1:
            index = song.find("(")
            song = song[:index]
        else:
            pass
    except IndexError:
        pass

    return song

# removing certain characters
def strippping_characters(song):
    char_list = ['„', '”', '"', '“', "'", "’", "/", ",", ":", "[", "]", "(", ")", "!", "      ", "    ", "  "]
    for char in char_list:
        if song.find(char) != -1:
            song = song.replace(char, " ")
        else:
            pass
    return song

# strippirng song values with apostrophe '"'
def strippping_apostrophe(song):
    if song.find('"') != -1:
        song = song.replace('"', "")
    else:
        pass
    return song

# strippirng space at the begining ' '
def strippping_space(song):
    try:
        if song[0] == " ":
            song = song.replace(' ', "", 1)
        else:
            pass

    except IndexError:
        pass
    except TypeError:
        pass
    return song

# strippirng space at the end ' '
def strippping_space_e(song):
    try:
        if song[-1] == " ":
            song = song[:-1]
        else:
            pass

    except IndexError:
        pass
    return song

if __name__ == "__main__":
    main()


