from utiles import tab_ids
from envoi import envoyer
from time import sleep

for dest in tab_ids.keys():
    for prio in range(1,7):
        sleep(1) #TODO : traiter l'exception quand on essaie d'envoyer trop de trucs en même temps
        envoyer(prio,dest,"hola")

