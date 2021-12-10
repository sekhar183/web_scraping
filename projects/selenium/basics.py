from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which

chrome_options = Options()
chrome_options.add_argument("--headless")
#chrome_options.add_argument('--log-level=1')

chrome_path = which('chromedriver')
driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
#print(chrome_path)
driver.get('https://duckduckgo.com')

search_input = driver.find_element_by_xpath("(//input[contains(@class, 'js-search-input')])[1]")
search_input.send_keys('My User Agent')
search_input.send_keys(Keys.ENTER)
print(driver.page_source)
#driver.find_element_by_id("search_button_homepage").click()

driver.close()