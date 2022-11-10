from utiles import tab_ids
from envoi import envoyer
from time import sleep

for prio in range(1,8):
    for dest in tab_ids.keys():
        sleep(1) #TODO : traiter l'exception quand on essait d'envoyer trop de trucs en même temps
        envoyer(prio,dest,"hola")

