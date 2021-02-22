import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

URL = "https://maple.gg/guild/luna/찹찹"
MEMBER_INFO = "https://maple.gg/u/"

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

# member_search_function
def member_search():
  frame = soup.select_one('#guild-content')
  e_characters = frame.select('section > div.mb-4.row.text-center > div')
  characters = frame.select('section > div:nth-child(5) > div')
  member_list = []

  master = True

  for ch in e_characters:
   if master == True:
     name = ch.select_one('section > div.member-grade.is-master > div > div:nth-child(1) > b > a').get_text()
     member_list.append([name])
     master = False
   else:
     name = ch.select_one('section > div.member-grade > div > div:nth-child(1) > b > a').get_text()
     member_list.append([name])

  for ch in characters:
    name = ch.select_one('section > div:nth-child(2) > b > a').get_text()
    member_list.append([name])

  return member_list

# memeber_information_extract_function
def extract_member_info(member_list):
  member_information_list = []
  for i in range(len(member_list)):
    member_name = member_list[i][0]
    member_url = MEMBER_INFO + str(member_name)

    result = requests.get(member_url)
    result_soup = BeautifulSoup(result.text,'html.parser')

    name = result_soup.select_one('#user-profile > section > div > div.col-lg-8 > h3 > b').get_text()
    level = result_soup.select_one('#user-profile > section > div > div.col-lg-8 > div.user-summary > ul > li:nth-child(1)').get_text()
    user_class = result_soup.select_one('#user-profile > section > div > div.col-lg-8 > div.user-summary > ul > li:nth-child(2)').get_text()
    if result_soup.select_one('#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div > div > div > h1') is not None:
      muleung_max = result_soup.select_one('#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div > div > div > h1').get_text()
      muleung_max2 = re.findall("\d+", str(muleung_max))
    else:
      muleung_max2 = ['0']
    if result_soup.select_one('#dohangHistoryTbody > tr:nth-child(1) > td:nth-child(2) > h5') is not None:
      muleung_recent = result_soup.select_one('#dohangHistoryTbody > tr:nth-child(1) > td:nth-child(2) > h5').get_text()
      muleung_recent2 = re.findall("\d+", str(muleung_recent))
      muleung_recent_year = result_soup.select_one('#dohangHistoryTbody > tr:nth-child(1) > td:nth-child(1) > span').get_text()
      muleung_recent_month_day = result_soup.select_one('#dohangHistoryTbody > tr:nth-child(1) > td:nth-child(1) > b').get_text()
      muleung_recent_date = muleung_recent_year + ' ' + muleung_recent_month_day
    else:
      muleung_recent2 = ['0']
      muleung_recent_date = '기록없음'
    
    member_information_list.append([name,level,user_class]+muleung_max2+muleung_recent2+[muleung_recent_date])

    print(f'길드원 정보 추출중..{i+1}/{len(member_list)}')
  return member_information_list

