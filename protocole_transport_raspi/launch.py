from api_reception import main as reception
from application import main as app
from multiprocessing import Process,Queue
# argument 0 : queue infinie 

# après moult essais, il arrive à faire un get sur la queue que depuis le même processus : chaque processus a une copie de la queue? 
# pourquoi dans le test ça marche alors? 

if __name__ == '__main__': # je sais pas à quoi ça sert car j'ai eu la flemme de lire la doc 
    q = Queue()
    proc_reception=Process(target=reception,args=(q,)) 
    proc_app=Process(target=app,args=(q,))
    proc_app.start()
    proc_reception.start()
    proc_reception.join()
    proc_app.join()