import sys
import subprocess
from time import sleep
from threading import Thread
from multiprocessing import Process, Manager

id_raspi = 0 
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
buffer = {key:[None]*nb_trames for key in keys}


def test_variables(id_dest,id_or,id_mes,seq,ack): 
    print("variables récupérées :")
    print("id_dest =",id_dest)
    print("id_or =",id_or)
    print("id_mes =",id_mes)
    print("seq =",seq)
    print("ack =",ack)


def test_buffer(id_or,id_mes):
    print("message placé dans le buffer : ")
    for txt in reversed(buffer[(id_or,id_mes)]):
        if txt != None : 
            print(txt)

def process_mess(mess,buffer):
    print("process message...")
    #récupérer les différents champs de l'en-tête dans des variables
    mess=mess.split(" ") ## TODO adapter au format des messages reçus par le candump 
    id_dest = int(mess[0])>>4
    #si le message est pas pour moi return 
    if id_dest != id_raspi:
        print("ce message n'est pas pour moi")
        return 
    #si le message est pour moi, traiter et mettre dans buffer 
    id_or = int(mess[0])&15 
    id_mes = int(mess[1])>>5
    seq = (int(mess[1])>>1)&15
    ack = int(mess[1])&1   
    # test_variables(id_dest,id_or,id_mes,seq,ack)
    buffer[(id_or,id_mes)][seq] = mess[2:]
    print("message processé!")
    return (id_or,id_mes)

def test_reception(): 
    print("--------------------------------test de la réception------------------------------------")

    # 0000 0001 001 0010 0
    print("appel de process mess avec en tête 0 1 1 2 0")
    process_mess("1 36 hola tu",buffer)
    print("\n")

    # 0100 0001 001 0010 0 
    print("appel de process mess avec en tête 4 1 1 2 0")
    process_mess("65 36 hola tu",buffer)
    print("\n")

    print("test de la mise dans le buffer")
    print("data envoyée : hola tu que tal kfjdjk")
    print("\n")

    # 0000 0001 001 0001 0 
    process_mess("1 34 que tal",buffer)
    print("\n")
    # 0000 0001 001 0000 0 
    (id_or,id_mes) = process_mess("1 32 kfjdjk",buffer)
    print("\n")
    test_buffer(id_or,id_mes)
    print("--------------------------------------------------------------------------------------------")

# réception 
def reception(buffer):
    reception = subprocess.Popen(["candump","any"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # reception=subprocess.Popen(['ping', 'geekflare.com'], stdout=subprocess.PIPE, text=True)
    while True: 
        output=reception.stdout.readline()
        if output:
            process_mess(output.strip(),buffer) #output.strip() est un string 

# ça serait top d'arriver à lancer l'appli comme un process mais en mettant le code dans un autre fichier sinon ça va être infâme 
# et sinon, je sais pas comment lui passer le buffer comme argument 
def main(): 
    proc_reception=Process(target=reception,args=(buffer,)) 
    proc_reception.start()
    proc_reception.join()

test_reception()