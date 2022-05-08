from email import message_from_binary_file
from api_envoi import main as envoyer
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
    sleep(4)
    if recevoir==message_vide: 
        return
    print(recevoir(q).data)