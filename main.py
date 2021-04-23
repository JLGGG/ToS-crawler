import gensim.parsing.preprocessing as gsp
from bs4 import BeautifulSoup
from gensim import utils
from selenium import webdriver
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def start_search():
    opt = webdriver.ChromeOptions()
    opt.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    driver = webdriver.Chrome(options=opt)
    # driver = webdriver.Chrome()

    # Query to obtain links
    query = 'Terms of Service'
    links = []  # Initiate empty list to capture final results
    # Specify number of pages on google search, each page has 10 links
    n_pages = 2
    # Sites including with [Sample, Template, What, Frontpage, Definition, Generator] should remove
    black_list = ['Sample', 'Template', 'What', 'Frontpage', 'Definition', 'Generator', 'Wikipedia']
    for page in range(1, n_pages):
        url = "http://www.google.com/search?q=" + query + "&start=" + str((page - 1) * 10)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Remove related questions
        for tag in soup.select('.ULSxyf'):
            tag.decompose()

        search = soup.select('.yuRUbf')

        for h in search:
            links.append({
                'Title': h.select_one('.LC20lb.DKV0Md').text,
                'Link': h.a.get('href'),
                'Flag': "false"
            })

    # Remove links that contain blacklist words
    for link in links:
        for black in black_list:
            # The find() method returns -1 if the value is not found.
            if link['Title'].find(black) >= 0:
                link['Flag'] = "true"
                break

    final_links = []
    for i, link in enumerate(links):
        if link['Flag'] == "false":
            final_links.append(link)

    return final_links, driver


def clean_text(s):
    # strip_tags: Removal of tags (like <html>...)
    # strip_punctuation: Removal of punctuation (like ',','.'!'...)
    # strip_multiple_whitespaces: Removal of multiple whitespaces in between texts
    # strip_numeric: Removal of numerics
    # remove_stopwords: Removal of stop words (such as 'at', 'to', 'the'...)
    # strip_short: Removal of very short words
    # stem_text: Stemming converting words to its root form (ex. played -> play)
    filters = [
        gsp.strip_tags,
        gsp.strip_punctuation,
        gsp.strip_multiple_whitespaces,
        gsp.strip_numeric,
        gsp.remove_stopwords,
        gsp.strip_short,
        gsp.stem_text
    ]

    # s = s.lower()
    s = utils.to_unicode(s)
    for f in filters:
        s = f(s)
    return s


def calculate_text(soup):
    whitelist = [
        'p',
        'li',
        'div',
    ]
    node = []

    text_elements = [t for t in soup.find_all(text=True) if t.parent.name in whitelist]
    for text in text_elements:
        node.append({
            'Length': len(text),
            'Content': text,
        })

    # Sort descending according to the amount of text in the DOM structure
    # node = sorted(node, key=itemgetter('Length'), reverse=True)

    df = pd.DataFrame(node)
    df_cut = df[df['Length'] > 100]
    # df_cut.sort_values(by='Length', inplace=True)
    # print(f'{df_cut.index.min()}, {df_cut.index.max()}')
    imin = df_cut.index.min()
    imax = df_cut.index.max()

    df_filtered = df.iloc[imin:imax]

    # print(df.head())
    # print(df.tail())

    print(imin, imax)

    print(df_filtered.head())
    print(df_filtered.tail())

    # plt.show()

    # plt.bar(range(len(node)), node, align='center')
    # plt.xticks(range(len(node)), node)
    #
    #
    # plt.show()
    return node


def enter_link(links, driver):
    documents = []
    i = 0
    for link in links:
        print(f'Go to {link["Link"]}')
        driver.get(link["Link"])
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # for script in soup(["script", "style"]):
        #     script.decompose()
        #
        # strips = list(soup.stripped_strings)
        # documents.append({
        #     'Index': i,
        #     'Text': strips,
        # })
        # i += 1

        # ---------------- Currently testing... -------------------
        documents.append(calculate_text(soup))
        documents.append("--------------------------------------------")
        #   print(len(soup.select('div')))

        driver.back()

    print(documents)
    driver.close()  # Close Chrome process
    return documents


# TODO hyperlink navigation
# TODO Code to calculate the amount of contents

def main():
    links, driver = start_search()
    documents = enter_link(links, driver)


# print(documents)
# print(len(links))


main()
