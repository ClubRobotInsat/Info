from can_bus import envoyer
from time import sleep
# test : lancer recevoir en parallèle 


for i in range(100000):
    print(i)
    envoyer(2,2,1,str(i)) # prio 2, dest herkulex, origine raspi 