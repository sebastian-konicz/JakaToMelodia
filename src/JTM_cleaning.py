from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import os
import re
import requests
import pandas as pd
import time
from openpyxl import load_workbook

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def main():
    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JTM\ListaPiosenekAll.xlsx')

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

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JTM\ListaPiosenekAllClean.xlsx', index=False, encoding='ISO-8859-1')

# removing key words
def key_words(song):
    word_list = ["los szcz.", "los szczęścia", "~dalej ", "~ dalej ", "~dalej~ ", "*dalej* ", "?", "????", "...",
                 "złote przeboje ", "złote przeboje", "1. ", "(perły polskiej piosenki)"]
    for word in word_list:
        if song.find(word) != -1:
            song = song.replace(word, "")
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
    char_list = ['„', '”', '"', '“', "'", "/", ",", ":", "[", "]", "(", ")", "!", "      ", "    ", "  "]
    for char in char_list:
        if song.find(char) != -1:
            print(song)
            song = song.replace(char, " ")
            print(song)
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
    return song

if __name__ == "__main__":
    main()


