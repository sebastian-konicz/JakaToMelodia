from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = r'C:\Users\kose9001\Desktop\JTM\chromedriver.exe'

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\interim\Lista_piosenek_youtube.xlsx')
    print(df_all.head())

    # concatenating song and artist for youtube search
    df_all["Song_concat"] = df_all.apply(lambda df: df['Song_correct'] + " " + df['Artist_correct'], axis=1)

    # getting youtube video id
    df_all["YT_link"] = df_all.apply(lambda df: youtube_search(df['Song_concat']), axis=1)

    # saving to excel file
    print('saving file')
    df_all.to_csv(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\20_ListaPiosenekYoutube.csv',
                    index=False, encoding='UTF-8') # ISO-8859-1

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

def youtube_search(search_value):
    try:
        search_value = str(search_value)

        driver = webdriver.Chrome(PATH)
        driver.get('https://www.youtube.com/results?search_query=' + search_value)

        video = driver.find_element_by_id('video-title')
        video_link = video.get_attribute('href')

        print(search_value)
        print(video_link)

        driver.quit()

    except IndexError:
        video_link = ""
    except ValueError:
        video_link = ""
    return video_link

if __name__ == "__main__":
    main()


