from bs4 import BeautifulSoup
import os
import re
import requests
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # Getti
    main_page = requests.get('http://www.jakatomelodia.fora.pl/font-color-ffcc66-listy-piosenek-z-programu-color,27/')
    html_main_page = BeautifulSoup(main_page.content, 'html.parser')
    links_years = html_main_page.find_all("a", class_='forumlink')

    href_years = []
    link_years = []
    for link in links_years:
        # link to site with all the months for a given year
        href_year = link.get('href')
        # adding link to list
        href_years.append(href_year)

        # vale of year in the link
        link_year = link.text
        # adding year value to list
        link_years.append(link_year)

    print(link_years)
    # creating tuple (year, link)
    link_tuple = zip(link_years, href_years)
    # sorting tuple and creating dictionary {year: link}
    sorted_dictionary = dict(sorted(link_tuple))
    print(sorted_dictionary)

    # #GETTING LINKS FOR ALL MONTHS IN A GIVEN YEAR
    # href_months = months(href_years)
    # print(href_months)

    dataframe_all = []
    # GETTING LINKS FOR ALL MONTHS IN A GIVEN YEAR
    for year, link in sorted_dictionary.items():
        print(year)
        print(link)
        href_months = months(link)

        # GETTING LINKS FOR ALL PAGES IN GIVEN MONTH
        # empty dataframe list
        dataframe_year = []
        for page in href_months:
            page_month, month_title = pages_month(page)

            # GETTING ALL POSTS FROM A PAGE IN GIVEN MONTH
            # empty dataframe list
            dataframe_month = []
            for page in page_month:
                print(page)
                post_month_page = posts_month(page)

                # GETTING DATAFRAMES FOR EACH POST
                # empty dataframe list
                dataframe_page = []
                # iterating throug posts in post_month_page
                for post in post_month_page:
                    text_post = text_extraction(post)
                    dataframe_post = dataframe_creation(text_post, month_title)
                    dataframe_page.append(dataframe_post)
                # concatenating page dataframe
                dataframe_page = pd.concat(dataframe_page)
                # reseting index
                dataframe_page = dataframe_page.reset_index(inplace=False, drop=True)
                # adding page dataframe to month dataframe list
                dataframe_month.append(dataframe_page)

            # concatenating month dataframe
            dataframe_month = pd.concat(dataframe_month)
            # reseting index
            dataframe_month = dataframe_month.reset_index(inplace=False, drop=True)
            dataframe_year.append(dataframe_month)

        # concatenating year dataframe
        dataframe_year = pd.concat(dataframe_year)
        # reseting index
        dataframe_year = dataframe_year.reset_index(inplace=False, drop=True)
        dataframe_all.append(dataframe_year)
        # saving to excel
        dataframe_year.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenek{year}.xlsx'.format(year=year), index=False, encoding='ISO-8859-1')

    dataframe_all = pd.concat(dataframe_all)
    # reseting index
    dataframe_all = dataframe_all.reset_index(inplace=False, drop=True)
    # saving to excel
    dataframe_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\ListaPiosenekAll.xlsx', index=False, encoding='ISO-8859-1')

    print("Program skończył działać")

# Function getting links for all months in a given year
def months(href_years):
    year_page = requests.get(href_years)
    html_year_page = BeautifulSoup(year_page.content, 'html.parser')
    links_months = html_year_page.find_all("a", class_='topictitle')

    href_months = []
    for link in links_months:
        href_month = link.get('href')
        href_months.append(href_month)

    # Returning list of links for all months and special edition episodes
    return href_months

# Function getting links for all pages in given month
def pages_month(href_months):
    month_page = requests.get(href_months)
    html_month_page = BeautifulSoup(month_page.content, 'html.parser')

    # getting month title
    month_title = html_month_page.find("a", class_='maintitle')
    month_title = month_title.text

    # getting html object with links
    links_month_pages = html_month_page.find_all("span", class_='gensmall')
    # retrieving links form object
    span_links = links_month_pages[0].find_all('a')

    href_month_pages = [href_months]
    for link in span_links:
        href_month_page = link.get('href')
        # print(href_month_page)
        href_month_pages.append(href_month_page)

    # Removing duplicate links
    href_months_pages = list(dict.fromkeys(href_month_pages))
    # Returning list of links for all months and special edition episodes
    return href_months_pages, month_title

# Function getting all the posts for pages in given month
def posts_month(page_month):
    posts_page = requests.get(page_month)
    html_posts_page = BeautifulSoup(posts_page.content, 'html.parser')

    # getting html object with post
    posts_body = html_posts_page.find_all("span", class_='postbody')
    return posts_body

# Function extracting text from post
def text_extraction(post):
    # getting ridd of <br> tags
    for br in post('br'):
        br.decompose()

    # getting ridd of <br> tags
    for span in post('span'):
        if span.text == None:
            pass
        else:
            span.replaceWith(span.text)

    # getting text form post
    post_text = post.text

    text = os.linesep.join([s for s in post_text.splitlines() if s])
    return text

# Function creating dataframe from post text
def dataframe_creation(post_text, month_title):
    song_data = []
    date = ""
    round = ""
    for line in post_text.splitlines():
        # changing text to lowercase
        line = line.lower()
        song = ""

        # Checking for date pattern
        patternDate = re.compile("([0-9]*\.[0-9]{2}\.[0-9]*)")
        if type(patternDate.search(line)) == re.Match:
            date = patternDate.search(line).group(1)
        else:
            pass

        # Checking for song pattern
        patternDate = re.compile("([0-9]{1}\.\s)")
        if type(patternDate.search(line)) == re.Match:
            song = line[3:]
        else:
            pass

        # Checking for round pattern
        patternRound = "runda"
        if line.find(patternRound) != -1:
            round = line[:9]
        else:
            pass

        # Checking for round pattern
        patternFinal = "fina"
        if line.find(patternFinal) != -1:
            round = "FINAŁ"
        else:
            pass

        # Checking for P: pattern
        patternP = "p:"
        if line.find(patternP) != -1:
            song = line[3:]
            round = "Początek"
        else:
            pass

        # Checking for K: pattern
        patternK = "k:"
        if line.find(patternK) != -1:
            song = line[3:]
            round = "Koniec"
        else:
            pass

        # adding data to list
        song_data.append([song, round, date, month_title])

    # creating dataframe
    song_dataframe = pd.DataFrame(song_data)
    # renaming dataframe columns
    print(song_dataframe)
    if song_dataframe.empty == True:
        pass
    else:
        song_dataframe.columns = ["Song", "Round", "Date", "Month"]
        # dropping empty song rows
        song_dataframe = song_dataframe.drop(song_dataframe[song_dataframe['Song'] == ''].index)
        # reseting index
        song_dataframe = song_dataframe.reset_index(inplace=False, drop=True)
    return song_dataframe

if __name__ == "__main__":
    main()


