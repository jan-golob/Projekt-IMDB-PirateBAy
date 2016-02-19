
import PretnarOsnova as pr
import re
#source https://ukpirate.org/s/?q=((interstellar))&video=on&category=0&page=0&orderby=99$


n=10

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

def raz_zanr(zanri):
    ys = []
    for y in zanri:
        ys.append(re.findall(r'<a href="/genre/(.*?)">', y))
    return ys
        
## http://www.imdb.com/search/title?count=100&release_date=2004,2014&sort=moviemeter&start={}&title_type=feature

Slovar_l = []
Slovar_z = []
for m in range(n):
    pr.shrani("http://www.imdb.com/search/title?count=100&release_date=2004,2014&sort=moviemeter&start={}&title_type=feature".format(m*100+1), "imdb_pop{}.txt".format(m), vsili_prenos=False)
    test = pr.html.unescape(pr.vsebina_datoteke("imdb_pop{}.txt".format(m)))
    imena = raz_imena(re.findall(r'<a href="/title/tt\d+/" title="(.*?)">', test))
    ocene = raz_ocene(re.findall(r'Users rated this (.*?)- click stars to rate', test))
    zanr = raz_zanr(re.findall(r'<span class="genre">(.*?)</span>', test))

    m_slovar=[]
    for i in range(len(imena)):
        m_slovar.append({"Id":m*100+i ,"ime":imena[i][0][0], "leto":imena[i][0][1], "IMDB_ocena":ocene[i][0][0], "IMBD_glasovi":int((ocene[i][0][1]).replace(",",""))})
    Slovar_l += m_slovar

    dvojci_z = []
    for i in range(len(zanr)):
        for j in zanr[i]:
            dvojci_z.append({"Id":m*100+i ,"zanr":j})
    Slovar_z += dvojci_z
            

##Slovar_l=[{'IMBD glasov': '820,170', 'Id': 1, 'IMDB ocena': '8.6', 'leto': '2014', 'ime': 'Interstellar'}]

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
    Slovar_l[j]["PBay_sejalci"]=sum(map(int,seed))
    Slovar_l[j]["PBay_pijavke"]=sum(map(int,leec))

print(Slovar_l)
print(Slovar_z)

pr.zapisi_tabelo(Slovar_l,["Id","ime","leto","IMDB_ocena","IMBD_glasovi", "PBay_sejalci", "PBay_pijavke"],"Podatki_Projekt.csv")
pr.zapisi_tabelo(Slovar_z,["Id","zanr"], "Zanr_projekt.csv")
