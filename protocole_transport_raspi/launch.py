from api_reception import main as reception
#import api_envoi
from application import main as app
from multiprocessing import Process, Manager


# nb de stm/raspi connectés
nb_disp=16
# nb de messages différents pouvant être envoyés en simultané par le même dispositif
nb_mess=8
# nb de trames max par message 
nb_trames = 16 
keys = [(id_or,id_mes) for id_or in range(nb_disp) for id_mes in range(nb_mess)]

# pour partager le buffer 
manager = Manager()
buffer = manager.dict()
# buffer pour l'application : dictionnaire avec key = (id_or,id_mes) 
# liste contenant les divers datas 
# sys.getsizeof(buffer)=4696
buffer = {key:[None]*nb_trames for key in keys}



if __name__ == '__main__':
    proc_app=Process(target=app,args=(buffer,))
    proc_reception=Process(target=reception,args=(buffer,)) 
    proc_reception=Process(target=reception,args=(buffer,))
    proc_reception.start()
    proc_app.start()
    proc_reception.join()
    proc_app.join()