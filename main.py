from bs4 import BeautifulSoup
from selenium import webdriver


def start_search():
    driver = webdriver.Chrome()

    # Query to obtain links
    query = 'Terms of Service'
    links = []  # Initiate empty list to capture final results
    # Specify number of pages on google search, each page has 10 links
    n_pages = 2
    for page in range(1, n_pages):
        url = "http://www.google.com/search?q=" + query + "&start=" + str((page - 1) * 10)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # TODO clear related questions
        # how to remove related questions?
        for tag in soup.select('div.ygGdYd related-question-pair'):
            tag.decompose()

        search = soup.select('.yuRUbf')

        for h in search:
            links.append({
                'Title': h.select_one('.LC20lb.DKV0Md').text,
                'Link': h.a.get('href'),
            })

    driver.close()  # Close Chrome process
    return links


# TODO hyperlink navigation
# TODO Code to calculate the amount of contents

def main():
    result = start_search()
    print(result)
    print(len(result))


main()
