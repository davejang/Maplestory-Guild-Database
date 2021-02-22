from function import member_search
from function import extract_member_info

import openpyxl

# Save to Excel File
member_list = member_search()
member_info = extract_member_info(member_list)
print(member_info)

database = openpyxl.Workbook()
sheet = database.active
sheet.append(['닉네임','직업/레벨','무릉 최고 층수','최근 무릉 기록','최근 무릉 기록 일자'])
for i in range(0,len(member_list),1):
  sheet.append([member_info[i][0],member_info[i][1],member_info[i][2],member_info[i][3],member_info[i][4],member_info[i][5]])
database.save('찹찹 길드원 현황.xlsx')

print("길드원 정보 추출에 성공하였습니다. xlsx파일로 저장합니다.")