import asyncio
import envoi 
import reception 
from threading import Thread 
from utiles import dict_events


# TODO test : lancer simulate_herkulex puis ce programme et vérifier si ça marche 
async def bouger_bras(mouvement):
    print("j'envoie le message " + mouvement)
    envoi.envoyer(2,2,1,mouvement)
    print("maintenant j'attends")
    envoi.attendre_confirmation(2,1,2,mouvement)
    print("j ai fini")



async def main():
    print("j'appelle bouger bras")
    tache = asyncio.create_task(bouger_bras("yo"))
    await tache
    print("coucou j'ai appelé la fonction")



dict_events={}
thread_reception = Thread(target=reception.recevoir, args=())
thread_reception.start()
asyncio.run(main())
thread_reception.join()


