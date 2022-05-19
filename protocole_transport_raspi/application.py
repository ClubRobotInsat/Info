from api_envoi import envoyer
from utiles import Message
from utiles import id_raspi


# pour créer un message à envoyer : message = Message(id_dest, id_raspi, data)
# l'id_mes est assignée automatiquement par le protocole

def main(q, ack_received, lock_buffer_acks, buffer_acks):  # ack_received et lock_buffer_acks doivent être passés à la méthode envoyer pour que la réception des acks se
    # passe bien
    while True:
        if not q.empty():
            print(q.get().data)  # get bloquant tant que la queue est vide!
