'''
# -*-coding:utf-8 -*
import sys  
reload(sys)
sys.setdefaultencoding('utf-8')
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
from string import digits

'''
w：新建檔案寫入(檔案可不存在，若存在則清空，適用於第一次寫入的資料)
a：資料附加到舊檔案後面(游標指在EOF)
'''

# 判斷是否為數字
def is_number(num):
  pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
  result = pattern.match(num)
  if result:
    return True
  else:
    return False

# 下載Course Outline內容
r = requests.get('http://class-qry.acad.ncku.edu.tw/syllabus/online_display.php?syear=0108&sem=2&co_no=F731700&class_code=')
r.encoding='big5'

Prerequisite = ""
Contact = ""
Grading = ""
Strategies = ""
Material = ""
References = ""
Description = ""
Objectives = ""
Outline = ""


# 確認是否下載成功
if r.status_code == requests.codes.ok:
    # 以 BeautifulSoup 解析 HTML 程式碼
    soup = BeautifulSoup(r.text, 'html.parser')
    divs = soup.find_all('div', 'block')

    for div in divs:

        if div.text.find('先修課程或先備能力') != -1:
            Prerequisite = div.text[1:]

        if div.text.find('教師聯絡資訊') != -1:
            Contact = div.text[1:]

        if div.text.find('參考書目') != -1:
            References = div.text[1:]

        if div.text.find('課程概述') != -1:
            Description = div.text[1:]

        if div.text.find('課程學習目標') != -1:
            Objectives = div.text[1:]

        if div.text.find('評量方式') != -1:
            #print(div.text)
            str = div.text.splitlines()
            index = len(str) - 3
            L1 = [None] * (index-6)
            L2 = [None] * (index-6)
            for i in range(6,index):
                num = ''.join([x for x in str[i] if x.isdigit()])
                L1[i-6] = str[i].replace(num,'')
            for i in range(7,index+1):
                num = ''.join([x for x in str[i] if x.isdigit()])
                L2[i-7] = num

            Grading = list(zip(L1,L2))

        if div.text.find('教學方法') != -1:
            #print(div.text)
            str = div.text.splitlines()  

            index = len(str) - 3
            L1 = [None] * (index-5)
            L2 = [None] * (index-5)
            for i in range(5,index):
                num = ''.join([x for x in str[i] if x.isdigit()])
                L1[i-5] = str[i].replace(num,'')
            for i in range(6,index+1):
                num = ''.join([x for x in str[i] if x.isdigit()])
                L2[i-6] = num

            Strategies = list(zip(L1,L2))

        if div.text.find('課程教材') != -1:
            #print(div.text)
            Material = div.text[1:]
           
        if div.text.find('課程進度') != -1:
            str = div.text.splitlines()[5]
            str=str.replace("10", "#")
            str=str.replace("11", "#")
            str=str.replace("12", "#")
            str=str.replace("13", "#")
            str=str.replace("14", "#")
            str=str.replace("15", "#")
            str=str.replace("16", "#")
            str=str.replace("17", "#")
            str=str.replace("18", "#")
            str=str.replace("1", "")
            str=str.replace("2", "#")
            str=str.replace("3", "#")
            str=str.replace("4", "#")
            str=str.replace("5", "#")
            str=str.replace("6", "#")
            str=str.replace("7", "#")
            str=str.replace("8", "#")
            str=str.replace("9", "#")
            str=str.replace("##", "#")

            a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
            b = str.split('#')

            Outline = list(zip(a,b))

    with open('result.csv', 'w', newline='') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
        writer.writerow(["先修課程或先備能力","教師聯絡資訊","評量方式","教學方法","課程教材","參考書目","課程概述","課程學習目標","課程進度"])
        writer.writerow([Prerequisite,Contact,Grading,Strategies,Material,References,Description,Objectives,Outline])
    csvfile.close()
