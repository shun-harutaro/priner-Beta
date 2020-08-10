import requests
from bs4 import BeautifulSoup
import datetime
import PyPDF2
import linecache
import urllib.request
from google.cloud import firestore

def scape(d,root):
    res = requests.get(root+f'wkprntans/index-f2{d}.html')
    soup = BeautifulSoup(res.text, 'html.parser')
    source = soup.find_all('a')
    links = [url.get('href') for url in source]
    texts = [url.get_text() for url in source]
    return links,texts

def correct(root,d,num,urls,texts):
    count=-1
    l=[]
    urls_in=[s for s in urls if d+str(num) in s]
    for n in urls_in:
        if count==-1:
            pass
        else:
            url = root+'/wkprntans/'+n
            savename = "print.pdf"
            urllib.request.urlretrieve(url, savename)
            with open(savename, "rb") as f:
                reader = PyPDF2.PdfFileReader(f)
                page = reader.getPage(0)
                text = page.extractText()
                line = text.splitlines()
                result = line[7]
            month,day=map(int,texts[count].split("/"))
            date=datetime.datetime(2020,month,day).strftime("%Y/%m/%d")
            index=[date,result]
            l.append(index)
        count+=1
    return l

while True:
    root = input("教員サイトのトップページのURLを入力(最後が'/◯◯2/'になるように)")
    d = input("学科を入力(m or i)")
    if d == "m" or d == "i":
        num = int(input("出席番号を入力(半角2ケタ)"))
        break
    else:
        print("不正な値です")
if d=="m":
    department="機械工学科"
else:
    department="情報工学科"

urls,texts = scape(d,root)
ml=correct(root,d,num,urls,texts)
print(f"{department} {num}番の該当正解数の推移")
for i in range(len(ml)):
    print(ml[i][0]+"=>%3d問"%int(ml[i][1]))
