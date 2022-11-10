# id en décimal

tab_noms= ["raspi", "herkulex", "base roulante"]


tab_ids={}
ind = 1
for nom in tab_noms:
    tab_ids[nom]=ind
    ind+=1

while ind <=15:
    tab_ids[ind]=ind
    ind+=1


print(tab_ids)
