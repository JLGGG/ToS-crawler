from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.google.com")
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("Terms of Service")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
v = soup.select('.yuRUbf')
for i in v:
    print(i.select_one('.LC20lb.DKV0Md').text)  # Title
    print(i.a.attrs['href'])  # Link
    print()

driver.close()  # Close Chrome process
