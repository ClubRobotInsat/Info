from api_envoi import main as envoyer
from utiles import Message
from time import sleep

def main(q):
    print("\n-----------------------------hello world--------------------------\n")
    print("J'attends...")
    sleep(1)
    print("j'ai fini d'attendre")
    # q.put("hello world")
    message=q.get() # le get est bloqué en attente visiblement, la queue est vide 
    print("j'ai bien pris la data")
    print("data reçue dans app : ",message.data)