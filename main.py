import os
import re
from pathlib import Path

import pandas as pd
# import random
import time
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from func_timeout import func_timeout, FunctionTimedOut


# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# import matplotlib.pyplot as plt


def start_search(query):
    opt = webdriver.ChromeOptions()
    opt.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    # opt.add_argument('headless')
    # caps = webdriver.DesiredCapabilities.CHROME.copy()
    # caps['acceptInsecureCerts'] = True
    driver = webdriver.Chrome("C:/Users/USER-PC/Downloads/chromedriver_win32/chromedriver.exe", options=opt)
    # driver = webdriver.Chrome("C:/Users/USER-PC/Downloads/chromedriver_win32/chromedriver.exe")

    # create action chain object
    # action = ActionChains(driver)

    # Query to obtain links
    # query = 'Terms of Service'
    links = []  # Initiate empty list to capture final results
    # Specify number of pages on google search, each page has 10 links
    n_pages = 35
    # Sites including with [Sample, Template, What, Frontpage, Definition, Generator] should remove
    black_list = ['sample', 'template', 'frontpage', 'definition', 'generator', 'clauses', 'abuse',
                  'what', 'agree', 'no', 'wikipedia', 'why', 'how', 'need', 'feed', 'not', 'click', 'spectrum']
    whitelist = ['terms', 'conditions', 'service', 'use']

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

        # action.move_by_offset(random.randrange(1,10), random.randrange(1,10))
        # action.perform()

        # try to bypass "I am not a robot".
        time.sleep(0.25)

    # Remove links that contain blacklist words
    for link in links:
        for black in black_list:
            # The find() method returns -1 if the value is not found.
            if link['Title'].lower().find(black) >= 0:
                link['Flag'] = "true"
                break

    final_links = []
    for i, link in enumerate(links):
        for white in whitelist:
            if link['Flag'] == "false" and link['Title'].lower().find(white) >= 0:
                final_links.append(link)
                break

    return final_links, driver


stop_words = set(stopwords.words('english'))
lemma = WordNetLemmatizer()


def clean_text(s):
    s = re.sub('[^a-zA-Z]', ' ', s)  # Removing numbers and punctuation
    s = str(s).lower()  # Convert all characters into lowercase
    s = word_tokenize(s)  # Tokenization
    s = [w for w in s if w not in stop_words]  # Removing stop words
    s = [lemma.lemmatize(word=w, pos='v') for w in s]  # Lemmatization
    s = [i for i in s if len(i) > 2]  # Remove the words having length <= 2
    s = ' '.join(s)  # Converting list to string
    return s


def collect_ToS_text(soup):
    whitelist = [
        'p',
        'li',
        'div',
        'span',
        'b',
        'a',
        'strong',
        'font',
    ]
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style',
        'title',
        # there may be more elements you don't want, such as "style", etc.
    ]
    node = []

    text_elements = [t for t in soup.find_all(text=True) if t.parent.name not in blacklist]
    text_elements = [t for t in text_elements if t.parent.name in whitelist]
    for text in text_elements:
        node.append({
            'Length': len(text),
            'Content': text,
        })

    df = pd.DataFrame(node)
    df_cut = df[df['Length'] > 100]

    # Text preprocessing
    df_cut_revised = df_cut.copy()
    df_cut_revised['Content'] = df_cut_revised['Content'].apply(clean_text)
    df_cut_revised['Length'] = df_cut_revised['Content'].apply(lambda x: len(x))
    final_df = df_cut_revised[df_cut_revised['Length'] > 10]

    # Visualization code
    # df.sort_values(by='Length', inplace=True, ascending=False)
    # df.plot(x='Content', y='Length')
    # plt.show()

    return final_df


def enter_link(links, driver, flag, duplicate_check, df):
    super_filename = 'whole.csv'

    i = 0
    for link in links:
        if link['Link'].find('.pdf') >= 0 or link['Link'].find('.html') >= 0:
            continue

        if flag == 0:
            duplicate_check.append(link["Link"])
        elif flag == 1:
            # Confirm already accessed link
            if link in duplicate_check:
                continue
        try:
            print(f'Go to {link["Link"]}')
            driver.get(link["Link"])
        except (NoSuchElementException, TimeoutException):
            continue

        try:
            soup = func_timeout(300, BeautifulSoup, args=(driver.page_source, 'html.parser'))
            # soup = BeautifulSoup(driver.page_source, 'html.parser')
        except FunctionTimedOut:
            print(f'{link["link"]} page use too many time. It is terminated.')
            continue

        # Save each web page, log file
        tdf = collect_ToS_text(soup)
        path = os.getcwd() + "/data/"
        sub_filename = f'{link["Title"]}.csv'
        sub_filename = re.sub("[\/:*?\"<>|]", "", sub_filename)
        tdf.to_csv(Path(path + sub_filename), index=False)  # save each page
        print(tdf)

        df = pd.concat([df, tdf])
        if i % 10 == 0:
            df.to_csv(Path(os.getcwd() + "/" + super_filename), mode='a', index=False)
        i += 1

        driver.back()

    df.to_csv(Path(os.getcwd() + "/" + super_filename), mode='a', index=False)  # save whole page's data
    print(f'Number of sentences collected: {len(df)}')
    driver.close()  # Close Chrome process


def main():
    duplicate_check = []
    df = pd.DataFrame(columns=['Length', 'Content'])
    links, driver = start_search('Terms of Service')
    enter_link(links, driver, 0, duplicate_check, df)
    links, driver = start_search('Terms of Conditions')
    enter_link(links, driver, 1, duplicate_check, df)


main()