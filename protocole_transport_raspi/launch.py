from api_reception import test_reception as reception
from application import main as app
from multiprocessing import Process, Queue, Condition
from api_envoi import test_envoi

if __name__ == '__main__':  # ne s'exécute que si le fichier est lancé directement (pas comme librairie)
    q = Queue()
    ack_received = Condition()
    proc_reception = Process(target=reception, args=(q, ack_received,))
    proc_app = Process(target=app, args=(q, ack_received))
    proc_test_envoi = Process(target=test_envoi, args=(ack_received, ) )
    proc_test_envoi.start()
    proc_reception.start()
    proc_app.start()
    proc_reception.join()
    proc_app.join()
    proc_test_envoi.join()
