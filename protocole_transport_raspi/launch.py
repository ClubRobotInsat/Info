from api_reception import test_reception as reception
from application import main as app
from threading import Thread
from queue import Queue
from api_envoi import test_envoi
from utiles import keys, buffer_acks
from threading import Condition
from time import sleep

if __name__ == '__main__':  # ne s'exécute que si le fichier est lancé directement (pas comme librairie)
    q = Queue(0) # 0 pour queue infinie
    ack_received_cond = Condition()
    thread_app = Thread(target=app, args=(q, buffer_acks,))
    thread_envoi = Thread(target=test_envoi, args=(buffer_acks, ack_received_cond))
    thread_reception = Thread(target=reception, args=(q, buffer_acks, ack_received_cond))
    thread_envoi.setDaemon(True) # le main attendra les threads
    thread_app.setDaemon(True)
    thread_reception.setDaemon(True)
    thread_reception.start()
    thread_app.start()
    thread_envoi.start()
    thread_reception.join()
    thread_app.join()
    thread_envoi.join()