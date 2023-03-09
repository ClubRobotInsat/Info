import asyncio
import sys
sys.path.append('/home/pi/Info/2022-2023/can_bus')
from manager import envoyer,attendre_confirmation,recevoir
from threading import Thread 


# test : lancer simulate_herkulex puis ce programme et vérifier si ça marche 
async def bouger_bras(mouvement):
    print("j'envoie le message " + mouvement)
    envoyer(2,2,1,mouvement)
    print("maintenant j'attends")
    attendre_confirmation(2,1,2,mouvement)
    print("j ai fini")



async def main():
    dict_events={}
    thread_reception = Thread(target=recevoir, args=())
    thread_reception.setDaemon(True)
    thread_reception.start()
    print("j'appelle bouger bras")
    tache = asyncio.create_task(bouger_bras("y"))
    await tache
    print("coucou j'ai appelé la fonction")




asyncio.run(main())


