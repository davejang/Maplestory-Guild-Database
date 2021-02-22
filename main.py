from function import member_search

import openpyxl

# Save to Excel File
list_temp = member_search()

database = openpyxl.Workbook()
sheet = database.active
sheet.append(['닉네임','직업/레벨'])
for i in range(0,len(list_temp),1):
  sheet.append([list_temp[i][0],list_temp[i][1]])
database.save('찹찹 길드원 현황.xlsx')

print("길드원 정보 추출에 성공하였습니다. xlsx파일로 저장합니다.")