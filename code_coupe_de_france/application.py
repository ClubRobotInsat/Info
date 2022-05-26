import lidar  # lidar
from api_envoi import envoyer
from utiles import Message
from utiles import id_raspi
from threading import Thread


# pour créer un message à envoyer : message = Message(id_dest, id_raspi, data)
# l'id_mes est assignée automatiquement par le protocole
# q sert à récupérer les messages reçus avec q.get()
# attention, fonction bloquante, vérifier avec q.empty()

# buffer_acks, ack_received_cond et buffer_lock doivent être passés à envoyer :
# envoyer(message, buffer_acks, ack_received_cond, buffer_lock)


def main(q, buffer_acks, ack_received_cond, buffer_lock):
    """laser = lidar.initialisation()
    thread_detection = Thread(target= lidar.detection, args=(laser, buffer_acks, ack_received_cond, buffer_lock))
    thread_detection.setDaemon(True)
    thread_detection.start()"""
    print("envoi d'un message à 3")
    envoyer(Message(3, id_raspi,
                    ['FF', 'EE', 'AA', 'AA', 'CC', 'BB', '01', '01', '01', '01', '01', '01', '01', '01', '01',
                     '01', '01', '01']), buffer_acks, ack_received_cond, buffer_lock)
    print("reception d'un message")


    # thread_detection.join()

    while True:
        if not q.empty():
            print("message reçu : ")
            print(q.get().data)
            q.task_done()  # ne pas oublier après avoir récupéré un message!


