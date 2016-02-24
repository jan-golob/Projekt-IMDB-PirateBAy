
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
        return x.replace("'", "").replace(":","").replace(" & ", " ")

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
        
# http://www.imdb.com/search/title?count=100&release_date=2004,2014&sort=moviemeter&start={}&title_type=feature

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
        m_slovar.append({"Id":m*100+i ,"ime":imena[i][0][0], "leto":imena[i][0][1], "IMDB_ocena":ocene[i][0][0], "IMDB_glasovi":int((ocene[i][0][1]).replace(",",""))})
    Slovar_l += m_slovar

    dvojci_z = []
    for i in range(len(zanr)):
        for j in zanr[i]:
            dvojci_z.append({"st":m*100+i ,"zanr":j})
    Slovar_z += dvojci_z


# Slovar_l=[{'IMDB glasovi': '820,170', 'Id': 1, 'IMDB ocena': '8.6', 'leto': '2014', 'ime': 'Interstellar'}]

for j in range(len(Slovar_l)):
    naslov_all = remove(Slovar_l[j]["ime"])
    naslov_all2 = naslov_all.split()
    if len(naslov_all2) == 1:
        naslov = naslov_all[0]
    elif naslov_all2[0] in ["The","A"]:
        naslov = naslov_all2[1]
    else:
        naslov = naslov_all2[0]

    pr.shrani("https://ukpirate.org/s/?q={}&video=on&category=0&page=0&orderby=99$".format(naslov_all), "PirateBay_temp.txt", vsili_prenos=True)
    with open('PirateBay_temp.txt', 'r', encoding="utf-8") as myfile:
        data=myfile.read().replace('\n', '')


    leto = remove(Slovar_l[j]["leto"])

    prenosi = re.findall(r'<td align="right">(\d*?)</td>', data)
    seed = []
    leec = []
    imena = re.findall(r'<div class="detName">			<a href="/torrent/\d*?/(.*?)class=',data)

    for i in range(0, len(prenosi), 2):
        if re.findall(leto,imena[i//2]) and re.findall(naslov,imena[i//2]):
            seed.append(prenosi[i])
            leec.append(prenosi[i+1])


    seedN=sum(map(int,seed))
    leecN=sum(map(int,leec))


    Slovar_l[j]["PBay_sejalci"]= seedN
    Slovar_l[j]["PBay_pijavke"]= leecN


print(Slovar_l)
print(Slovar_z)

pr.zapisi_tabelo(Slovar_l,["Id","ime","leto","IMDB_ocena","IMDB_glasovi", "PBay_sejalci", "PBay_pijavke"],"Podatki_Projekt.csv")
pr.zapisi_tabelo(Slovar_z,["st","zanr"], "Zanr_projekt.csv")
