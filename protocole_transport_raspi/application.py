import utiles
from api_envoi import envoyer
from utiles import Message, Trame
import subprocess
from utiles import id_raspi


# pour créer un message à envoyer : message = Message(id_dest, id_raspi, data)
# l'id_mes est assignée automatiquement par le protocole
# q sert à récupérer les messages reçus avec q.get()
# attention, fonction bloquante, vérifier avec q.empty()

# buffer_acks et ack_received_cond doivent être passés à envoyer :
# envoyer(message, buffer_acks, ack_received_cond)

def main(q, buffer_acks, ack_received_cond, buffer_lock):
    print("envoi d'un message à 3")
    envoyer(Message(3, 0,
                    ['FF', 'EE', 'AA', 'AA', 'CC', 'BB', '01', '01', '01', '01', '01', '01', '01', '01', '01',
                     '01', '01', '01']), buffer_acks, ack_received_cond, buffer_lock)

    # je m'envoie mes propres acks, oui c'est moche

    subprocess.Popen(["cansend", "can0", "000#03 03 00 00 00 00 00 00"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)


    subprocess.Popen(["cansend", "can0", "000#03 01 00 00 00 00 00 00"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)


    subprocess.Popen(["cansend", "can0", "000#03 05 00 00 00 00 00 00"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

    while True:
        if not q.empty():
            print("message reçu : ")
            print(q.get().data)
            q.task_done()  # ne pas oublier après avoir récupéré un message!

