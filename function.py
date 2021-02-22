from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

URL = "https://maple.gg/guild/luna/찹찹"

# chrome driver setting
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# url response

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(3)
driver.get(URL)
driver.find_element_by_xpath('//*[@id="btn-sync"]').click()

# alert handling
driver.switch_to.alert.accept()

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

def member_search():
  frame = soup.select_one('#guild-content')
  e_characters = frame.select('section > div.mb-4.row.text-center > div')
  characters = frame.select('section > div:nth-child(5) > div')
  member_list = []

  master = True

  for ch in e_characters:
   if master == True:
     name = ch.select_one('section > div.member-grade.is-master > div > div:nth-child(1) > b > a').get_text()
     class_and_lv = ch.select_one('section > div.member-grade.is-master > div > div:nth-child(2) > span').get_text()
     member_list.append([name,class_and_lv])
     master = False
   else:
     name = ch.select_one('section > div.member-grade > div > div:nth-child(1) > b > a').get_text()
     class_and_lv = ch.select_one('section > div.member-grade > div > div:nth-child(2) > span').get_text()
     member_list.append([name,class_and_lv])

  for ch in characters:
    name = ch.select_one('section > div:nth-child(2) > b > a').get_text()
    class_and_lv = ch.select_one('section > div:nth-child(3) > span').get_text()
    member_list.append([name,class_and_lv])

  return member_list