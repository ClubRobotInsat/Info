from api_reception import main as reception
from application import main as app
from buffer import buffer
from multiprocessing import Process



if __name__ == '__main__': # je sais pas à quoi ça sert car j'ai eu la flemme de lire la doc 
    proc_app=Process(target=app,args=(buffer,))
    proc_reception=Process(target=reception,args=(buffer,)) 
    proc_reception=Process(target=reception,args=(buffer,))
    proc_reception.start()
    proc_app.start()
    proc_reception.join()
    proc_app.join()