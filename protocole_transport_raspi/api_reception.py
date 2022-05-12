import subprocess
from utiles import Trame,Message,buffer
from utiles import id_raspi


# pour tester 
###############################################################################################################

def print_ligne_buff(id_or,id_mes):
    print("(",id_or,",",id_mes,") : ")
    for mess in buffer[(id_or,id_mes)]:
        if mess != None : 
            print(mess.data)

def test_variables(trame): 
    print("variables récupérées :")
    print("id_dest =",trame.id_dest)
    print("id_or =",trame.id_or)
    print("id_mes =",trame.id_mes)
    print("seq =",trame.seq)
    print("ack =",trame.ack)

def test_reception(q,q_envoi): 
    print("--------------------------------test de la réception------------------------------------")

    # 0100 0001 001 0010 0 
    print("appel de process mess avec en tête 4 1 1 2 0")
    process_mess("can0 001 [8] FF 24 01 01 01 01 01 01",q,q_envoi)
    print("\n")

    # 0000 0001 001 0010 0
    print("appel de process mess avec en tête 0 1 1 2 0")
    process_mess("can0 001 [8] 01 24 01 01 01 01 01 01",q,q_envoi)
    print("\n")

    print("test de la mise dans le buffer")
    
    print("\n")
    
    # 0000 0001 001 0000 0 
    (id_or,id_mes) = process_mess("can0 001 [8] 01 20 01 01 01 01 01",q,q_envoi)
    print("\n")

    # 0000 0001 001 0001 0 
    process_mess("can0 001 [8] 01 22 01 01 01 01 01",q,q_envoi)
    print("\n")
    # print_ligne_buff(id_or,id_mes)


    # TODO : more tests 

    print("--------------------------------------------------------------------------------------------")

###############################################################################################################


# TODO : processer les ack
def process_mess(trame,q,q_envoi):
    print("process Trame...")
    trame=Trame(trame[17:]) # pour virer l'en tête du candump, j'ai trouvé que c'était 17 de façon empirique 
    test_variables(trame)
    #si la trame est pas pour moi return 
    if trame.id_dest != id_raspi:
        print("ce message n'est pas pour moi")
        return 
    # si le message est un ack, on le passe à l'api d'envoi 
    if trame.ack==1: 
        q_envoi.put(trame)
        return 
    #si le message est pour moi, traiter et mettre dans buffer  
    ligne_buff = buffer[(trame.id_or,trame.id_mes)]
    if not ligne_buff:
        ligne_buff.append(trame)
    elif ligne_buff[-1].seq < trame.seq: # trames pas dans l'ordre 
        dernier = ligne_buff[-1]
        ligne_buff[-1] = trame
        ligne_buff.append(dernier)
    else: 
        ligne_buff.append(trame)
    # message reçu en entier : 
    # dernière trame reçue (seq == 0) et toutes les trames sont là 
    if ((ligne_buff[-1].seq==0) and (len(ligne_buff)==ligne_buff[0].seq+1)): 
        message=Message(trame.id_dest,trame.id_or,trame.id_mes)
        q.put(message)

    print("Trame processée!")
    return (trame.id_or,trame.id_mes) #pour débug 


def reception(q,q_envoi):
    reception = subprocess.Popen(["candump","any"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    while True: 
        output=reception.stdout.readline()
        if output:
            process_mess(output.strip(),q,q_envoi) #output.strip() est un string 

