from utiles import tab_ids
from envoi import envoyer


for prio in range(1,8):
    for dest in tab_ids.keys():
        envoyer(prio,dest, "hola")

