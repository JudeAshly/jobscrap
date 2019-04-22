from bs4 import BeautifulSoup
import requests
import sqlite3
con=sqlite3.connect('tact.db')
cur=con.cursor()
b_url='https://www.indeed.ca/jobs?q=data+scientist&l=Toronto%2C+ON&start=20'
req = requests.get(b_url)
soup = BeautifulSoup(req.content,'html5lib')
d=soup.find_all(attrs={'target':'_blank'})
parm = re.findall(r"/rc.{60}",str(d))
param = [dx.replace(';','&') for dx in parm]

cur.execute("create table if not exists test3 (ID INTEGER PRIMARY KEY AUTOINCREMENT, Title text,Company_name text,link varchar(90),location varchar(50),Content TEXT)")
for url in param:
    request = requests.get(f"https://www.indeed.ca/{url}")
    soop=BeautifulSoup(request.content,'html5lib')
    title=soop.find('h3').get_text()
    #print(title)
    location=soop.find('span',attrs={'class':'icl-JobResult-jobLocation'}).get_text()
    #print(location)
    link=re.findall(r"https:.{69}",str(soop.find('a',attrs={'class':'icl-Button icl-Button--primary icl-Button--block'})))
    titl=soop.find('h4').get_text()
    #print(titl)
    #ds=soop.find('a',attrs={'class':'icl-Button icl-Button--primary icl-Button--block'})
    try:
        link[0]
    except:
        link=['NULL']
    content=soop.find('div',attrs={'id':'jobDescriptionText'}).get_text()
    #print(content)
    cur.execute("INSERT INTO test3 VALUES(NULL,?,?,?,?,?)",(title,titl,str(link[0]),location,content))
con.commit()
con.close()
    
