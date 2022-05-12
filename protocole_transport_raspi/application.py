
from api_envoi import envoyer
from utiles import Message
from time import sleep


message_vide = Message(-1,-1)


# récupère et renvoie le message dans q 
# renvoie message_vide si rien dans q 
def recevoir(q):
    if q.empty():
        return message_vide 
    else:
        return q.get()


def main(q):
    while(1):
        print(q.get().data)
