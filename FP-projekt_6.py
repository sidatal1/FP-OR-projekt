#Program kot vhodne podatke sprejme seznam v katerem navedemo za katere dimenzije želimo dobiti podatke,
#število korakov slučajnega sprehoda ter kolikokrat naj se ponovi slučajni sprehod za določeno dimenzijo.
#Kot rezultat nam program naredi .xlsx dokument v katerem dobimo tabelo z vrednostmi:
# - povprečna oddaljenost od izhodišča (program vzame povprečno oddaljenost od izhodišča v vsakem sprehodu in izračuna povprečje)
# - povprečna največja oddaljenost od izhodišča (program vzame najdaljšo razdaljo v vsaki ponovitvi in izračuna povprečje)
# - najdaljša razdalja (program vrne najdaljšo razdaljo, ki jo je zabeležil v vsah ponovitvah slučajnega sprehoda)
# - število vrnitev v izhodišče (program vrne v koliko ponovitvah slučajnega sprehoda smo se vrnili v izhodišče)
# - povprečno število srečanj (program vrne kolikokrat sta se v povprečju srečala slučajna sprehoda, torej program dobi seznam
#                              v katerem so števila srečanj za posamezno dimenzijo in izračuna povprečje)
# - v koliko ponovitvah se srečata (program nam pove v koliko ponovitvah sta se slučajna sprehoda srečala, ni pa pomembno kolikokrat sta se 
#                                   srečala v posamezni ponovitvi)

import random
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.function_base import average
import xlsxwriter
import seaborn as sns


#Funkcija enake_ver sprejme dimenzijo in število korakov slučajnega sprehoda ter nam vrne seznam seznamov, 
#kjer vsak podseznam vsebuje koordinate točke do katere smo prišli s slučajnim sprehodom.
def enake_ver(d,st_korakov):
    koraki=range(st_korakov)
    krajisce=[0] * d
    seznam=[[0] * d]
    for i in koraki:
        a = random.randint(0,1)
        b = random.randint(0,d-1)
        c=[]
        if a==0:
            krajisce[b] = krajisce[b] - 1
        else:
            krajisce[b] = krajisce[b] + 1
        for y in krajisce:
            c.append(y)
        seznam.append(c)
    return seznam

#Funkcija slovar sprejme seznam seznamov iz prejšnjih dveh funkcij ter naredi slovar v katerem so ključi točke slučajnega sprehoda, kot
#vrednosti pa vrne seznam, ki vsebuje oddaljenost točke od izhodišča, kolikokrat se je slučajni sprehod znašel v tej točki ter čas, ko 
# se je znašel tam.
def slovar(seznam):
    slovar = {}
    a=0
    for x in seznam:
        a=a+1
        razdalja = 0
        cas={}
        if str(x) in slovar.keys():
            e=slovar[str(x)]
            b=e[2]
            b[str(a)]=a
            slovar[str(x)]=[e[0],e[1]+1,b]
        else:
            cas[str(a)]=a
            for y in x:
                razdalja = razdalja + abs(y) 
                slovar[str(x)] = [razdalja,1,cas]
    return(slovar)

#Tukaj se začne program. Potrebno je določiti dimenzije za katere želimo dobiti izračun,
#kolikokrat ponovimo slučajni sprehod in število korakov slučajnega sprehoda. 
dimenzije=[1,10,50,100]
st_ponovitev=40
st_korakov=200
pov_oddaljenost=[]
pov_max_oddaljenost1=[]
srecanje1=[]
max_oddaljenost1=[]
vrnemo1=[]
srecanje3=[]

#Izračun se ponovi za vsako dimenzijo.
for dim in dimenzije: 

    vrnemo=0
    slovar2={}
    max_oddaljenost=0
    pov_max_oddaljenost=[]
    srecanje=[]
    srecanje2=0
    #Zanka nam naredi toliko slučajnih sprehodov kot smo nastavili st_ponovitev.
    for x in range(st_ponovitev):
        a1=enake_ver(dim,st_korakov)
        c=slovar(a1)
        #Izračunamo kolikokrat se vrnemo v izhodišče v slučajnem sprehodu.
        kolikokrat_v_izhodisce=(c[str([0] * dim)])[1]
        if kolikokrat_v_izhodisce>1:
            vrnemo = vrnemo + 1

    #Gledamo, ali se dva slučajna sprehoda, ki začneta hkrati v izhodišču srečata ter kolikokrat se srečata.
        seznam3=[]
        k=0
        e=enake_ver(dim,st_korakov)
        f=slovar(e)
        #Naredimo seznam tisith točk v katerih sta se nahajala oba.
        for x in f.keys():
            for y in c.keys():
                if x==y:
                    seznam3.append(x)
        #Pogledamo če sta bila v isti toči ob istem času.
        for x in seznam3:
            for y in ((c[x])[2]):
                if y in ((f[x])[2]):
                    k=k+1
        srecanje.append(int(k)-1)
        if k>1:
            srecanje2 +=1
    

        a=[]        
        g=[]
        h=0
        for y in c.values():
            #Največja razdalja od izhodišča v vseh ponovitvah.
            d=y[0]
            if d>max_oddaljenost:
                max_oddaljenost=d
            #Največjo razdaljo od izhodišča v vsaki ponovitvi posebaj je enaka h.
            if d>h:
                h=d
            #Naredimo slovar, kjer so ključi razdalje od izhodišča, vrednosti pa kolikokrat se je pojavila ta razdalja.
            if not str(d) in slovar2.keys():
                slovar2[str(d)]=0 #če te razdalje še ni v slovarju jo dodamo in nastavimo vrednost na nič
            a=list(g)
            for i in c.values():
                if i[0]==d: #gremo čez vse razdalje, ki smo jih dobili iz generiranega slučajnega sprehoda in gledamo, kdaj je ta razdalja enaka d
                    if not str(i[0]) in a: #pogledamo, če te razdalje še nismo upoštevali
                        slovar2[str(d)]=slovar2[str(d)] + i[1] #dodamo kolikorat se je še pojavila ta razdalja
                        g.append(str(i[0]))

        pov_max_oddaljenost.append(int(h))

    #naredimo seznam, kjer je vsaka razdalja podana tolikokrat, kot je bila v povprečju zastopana v vsaki ponovitvi
    seznam2=[]
    for x in slovar2.keys():
        seznam2=seznam2+([int(x)]*(round((slovar2[x])/st_ponovitev)))

    #Narišemo graf porazdelitve razdalje točk od izhodišča.
    fig = plt.figure()
    sns.ecdfplot(seznam2,color="red")
    plt.title("d{}".format(str(dim)))
    plt.ylabel('F(x)')
    plt.xlabel('Razdalja od izhodišča')
    fig.set_size_inches(5, 5)
    plt.savefig('graf{}.png'.format(str(dim)))

    #Izračunamo povprečne vrednosti ter shranimo željene vrednosti v nov seznam, kjer prva komponenta seznama sedaj predstavlja
    #podatke za dimenzijo 1 oziroma za tisto dimezijo, ki smo jo v seznamu "dimenzije" navedli kot prvo.
    pov_oddaljenost.append(round(average(seznam2),1))
    pov_max_oddaljenost1.append(round(average(pov_max_oddaljenost),1))
    srecanje1.append(round(average(srecanje),2))
    max_oddaljenost1.append(max_oddaljenost)
    vrnemo1.append(round((vrnemo),1))
    srecanje3.append(int(srecanje2))


seznam4=[pov_oddaljenost,pov_max_oddaljenost1,max_oddaljenost1,vrnemo1,srecanje1,srecanje3]


#Vse podatke ter grafe shranimo v .xlsx obliko.
workbook = xlsxwriter.Workbook('naloga_dodatno5.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
worksheet.write('A1',"Število ponovitev slučajnega sprehoda",bold)
worksheet.write('A2',"Število korakov v posameznem slučajnem sprehodu",bold)
worksheet.write('A4',"Postavke",bold)
worksheet.write('A5',"Povprečna oddaljenost od izhodišča",bold)
worksheet.write('A6',"Povprečna največja oddaljenost",bold)
worksheet.write('A7',"Najdaljša razdalja",bold)
worksheet.write('A8',"Število vrnitev v izhodišče",bold)
worksheet.write('A9',"Povprečno število srecanj (upoštevamo, da se lahko večkrat srečata v eni ponovitvi)",bold)
worksheet.write('A10',"V koliko ponovitvah se srečata",bold)
worksheet.write('B1',st_ponovitev,bold)
worksheet.write('B2',st_korakov,bold)
worksheet.write('B4',"d1",bold)
worksheet.write('C4',"d2",bold)
worksheet.write('D4',"d3",bold)
worksheet.write('E4',"d5",bold)
worksheet.write('F4',"d10",bold)
worksheet.write('G4',"d50",bold)
vrstica=3
for x in seznam4:
    vrstica +=1
    stolpec=0
    for y in x:
        stolpec +=1
        worksheet.write(vrstica,stolpec,y)
stolpec=1
vrstica=11
for x in dimenzije:
    worksheet.insert_image(vrstica,stolpec,'graf{}.png'.format(str(x)))
    stolpec +=8
workbook.close()




