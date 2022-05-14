
from api_envoi import envoyer
from utiles import Message
from time import sleep



def main(q):
    while(1):
        if not q.empty():
            print(q.get().data) # get bloquant tant que la queue est vide! 
