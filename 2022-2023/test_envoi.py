from utiles import tab_ids
from envoi import envoyer
from time import sleep

for dest in tab_ids.keys():
    for prio in range(1,7):
        for i in range(500): # testons notre programme
            envoyer(prio,dest,"hola")

