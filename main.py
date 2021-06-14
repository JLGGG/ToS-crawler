import os
import re
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from selenium import webdriver


# import matplotlib.pyplot as plt


def start_search():
    opt = webdriver.ChromeOptions()
    opt.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    opt.add_argument('headless')
    driver = webdriver.Chrome(options=opt)
    # driver = webdriver.Chrome()

    # Query to obtain links
    query = 'Terms of Service'
    links = []  # Initiate empty list to capture final results
    # How do I find the endpoint of crawler? Collect documents about 200k
    # No search endpoint. I just will collect documents about 200k amount.
    # Specify number of pages on google search, each page has 10 links
    n_pages = 3
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
    ]
    node = []

    text_elements = [t for t in soup.find_all(text=True) if t.parent.name in whitelist]
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


def enter_link(links, driver):
    df = pd.DataFrame(columns=['Length', 'Content'])
    super_filename = 'whole.csv'

    i = 0
    for link in links:
        print(f'Go to {link["Link"]}')
        driver.get(link["Link"])
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Save each web page, log file
        tdf = collect_ToS_text(soup)
        path = os.getcwd() + "/data/"
        sub_filename = f'{link["Title"]}.csv'
        tdf.to_csv(Path(path + sub_filename), index=False)  # save each page
        print(tdf)

        df = pd.concat([df, tdf])
        if i % 10 == 0:
            df.to_csv(Path(os.getcwd() + "/" + super_filename), index=False)
        i += 1

        driver.back()

    df.to_csv(Path(os.getcwd() + "/" + super_filename), index=False)  # save whole page's data
    print(f'Number of sentences collected: {len(df)}')
    driver.close()  # Close Chrome process


def main():
    links, driver = start_search()
    enter_link(links, driver)


main()
