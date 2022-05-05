from api_reception import main as reception
from application import main as app
from multiprocessing import Process

# TODO : créer la file de priorité 

if __name__ == '__main__': # je sais pas à quoi ça sert car j'ai eu la flemme de lire la doc 
    proc_app=Process(target=app)
    proc_reception=Process(target=reception) 
    proc_reception.start()
    proc_app.start()
    proc_reception.join()
    proc_app.join()