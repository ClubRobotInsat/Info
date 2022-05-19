from api_reception import test_reception as reception
from application import main as app
from multiprocessing import Process, Queue, Condition, Lock, Manager
from api_envoi import test_envoi
from utiles import keys
from time import sleep

if __name__ == '__main__':  # ne s'exécute que si le fichier est lancé directement (pas comme librairie)
    q = Queue()
    manager = Manager()
    buffer_acks = manager.dict()
    buffer_acks = {key: 0 for key in keys}
    proc_app = Process(target=app, args=(q, buffer_acks, ))
    proc_test_envoi = Process(target=test_envoi, args=(buffer_acks, ))
    proc_reception = Process(target=reception, args=(q, buffer_acks, ))
    proc_test_envoi.start()
    proc_reception.start()
    proc_app.start()
    proc_reception.join()
    proc_app.join()
    proc_test_envoi.join()
