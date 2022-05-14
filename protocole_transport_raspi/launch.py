from api_reception import test_reception as reception
from application import main as app
from api_envoi import process_ack 
from multiprocessing import Process,Queue


if __name__ == '__main__':# ne s'exécute que si le fichier est lancé directement (pas comme librairie) 
    q = Queue()
    q_envoi= Queue()
    proc_reception=Process(target=reception,args=(q,q_envoi,)) 
    proc_app=Process(target=app,args=(q,))
    # proc_envoi=Process(target=process_ack,args=(q_envoi,))
    proc_reception.start()
    proc_app.start()
    # proc_envoi.start()
    proc_reception.join()
    proc_app.join()
    # proc_envoi.join()