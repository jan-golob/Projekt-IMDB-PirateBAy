
import PretnarOsnova as pr
import re
#source https://ukpirate.org/s/?q=((interstellar))&video=on&category=0&page=0&orderby=99$


n=7

def remove(x):
    if x == "Birdman or (The Unexpected Virtue of Ignorance)":
        return "Birdman"
    elif x == "Mission: Impossible - Ghost Protocol":
        return "Ghost Protocol"
    else:
        return x.replace("'", " ").replace(":"," ").replace("&", " ")

def raz_ocene(oce):
    xs = []
    for x in oce:
        xs.append(re.findall(r'(.*?)/10.*?(\d.*?) votes', x))
    return xs

def raz_imena(im):
    xs = []
    for x in im:
        xs.append(re.findall(r'(.*?)\s.(\d\d\d\d)', x))
    return xs


Slovar_l=[]
for m in range(n):
    pr.shrani("http://www.imdb.com/search/title?at=0&release_date=2009,2014&sort=moviemeter&start={}&title_type=feature".format(m*50+1), "imdb_pop{}.txt".format(m), vsili_prenos=False)
    test = pr.html.unescape(pr.vsebina_datoteke("imdb_pop{}.txt".format(m)))
    imena = raz_imena(re.findall(r'<a href="/title/tt\d+/" title="(.*?)">', test))
    ocene = raz_ocene(re.findall(r'Users rated this (.*?)- click stars to rate', test))

    m_slovar=[]
    for i in range(len(imena)):
        m_slovar.append({"št":m*50+i+1 ,"ime":imena[i][0][0], "leto":imena[i][0][1], "IMDB ocena":ocene[i][0][0], "IMBD glasov":ocene[i][0][1]})
    Slovar_l += m_slovar
    

##Slovar_l=[{'IMBD glasov': '820,170', 'št': 1, 'IMDB ocena': '8.6', 'leto': '2014', 'ime': 'Interstellar'}]

for j in range(len(Slovar_l)):
    pr.shrani("https://ukpirate.org/s/?q={}&video=on&category=0&page=0&orderby=99$".format(remove(Slovar_l[j]["ime"])), "PirateBay_temp.txt", vsili_prenos=True)
    with open('PirateBay_temp.txt', 'r', encoding="utf-8") as myfile:
        data=myfile.read().replace('\n', '')

    prenosi = re.findall(r'<td align="right">(\d*?)</td>', data)
    seed = []
    leec = []
    for i in range(0, len(prenosi), 2):
        seed.append(prenosi[i])
        leec.append(prenosi[i+1])
    Slovar_l[j]["PirateBay sejalci"]=sum(map(int,seed))
    Slovar_l[j]["PirateBay pijavke"]=sum(map(int,leec))

print(Slovar_l)

pr.zapisi_tabelo(Slovar_l,["št","ime","leto","IMDB ocena","IMBD glasov", "PirateBay sejalci", "PirateBay pijavke"],"Podatki_Projekt.csv")
