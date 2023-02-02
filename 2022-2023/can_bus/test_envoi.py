from utiles import tab_ids
from envoi import envoyer
from time import sleep

for i in range(100000):
    print(i)
    envoyer(2,2,1,str(i)) # prio 2, dest herkulex, origine raspi 