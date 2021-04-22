from bs4 import BeautifulSoup
from selenium import webdriver


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
    black_list = ['Sample', 'Template', 'What', 'Frontpage', 'Definition', 'Generator']
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


def enter_link(links, driver):
    documents = []
    i = 0
    for link in links:
        print(f'Go to {link["Link"]}')
        driver.get(link["Link"])
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for script in soup(["script", "style"]):
            script.decompose()

        strips = list(soup.stripped_strings)
        documents.append({
            'Index': i,
            'Text': strips,
        })
        i += 1
        driver.back()

    driver.close()  # Close Chrome process
    return documents


# TODO hyperlink navigation
# TODO Code to calculate the amount of contents

def main():
    links, driver = start_search()
    documents = enter_link(links, driver)
    print(documents)
    print(len(links))


main()
