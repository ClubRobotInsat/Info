import subprocess
from utiles import Trame,Message,buffer

id_raspi = 0 


# pour tester 
###############################################################################################################

def print_ligne_buff(id_or,id_mes):
    print("(",id_or,",",id_mes,") : ")
    for mess in buffer[(id_or,id_mes)]:
        if mess != None : 
            print(mess.data)

def test_variables(id_dest,id_or,id_mes,seq,ack): 
    print("variables récupérées :")
    print("id_dest =",id_dest)
    print("id_or =",id_or)
    print("id_mes =",id_mes)
    print("seq =",seq)
    print("ack =",ack)

def test_reception(q): 
    print("--------------------------------test de la réception------------------------------------")

    # 0100 0001 001 0010 0 
    print("appel de process mess avec en tête 4 1 1 2 0")
    process_mess("65 36 hola tu",q)
    print("\n")

    # 0000 0001 001 0010 0
    print("appel de process mess avec en tête 0 1 1 2 0")
    process_mess("1 36 hola tu",q)
    print("\n")

    print("test de la mise dans le buffer")
    print("data envoyée dans le désordre: hola tu que tal kfjdjk")
    print("\n")
    
    # 0000 0001 001 0000 0 
    (id_or,id_mes) = process_mess("1 32 kfjdjk",q)
    print("\n")

    # 0000 0001 001 0001 0 
    process_mess("1 34 que tal",q)
    print("\n")
    # print_ligne_buff(id_or,id_mes)


    # TODO : more tests 

    print("--------------------------------------------------------------------------------------------")

###############################################################################################################


# TODO : processer les ack
def process_mess(trame,q):
    print("process Trame...")
    trame=trame.split(" ") ## TODO adapter au format des trames reçus par le candump, 
    # et peut-être aussi vérifier que le format du string reçu est le bon  
    trame=Trame(trame)
    #si la trame est pas pour moi return 
    if trame.id_dest != id_raspi:
        print("ce message n'est pas pour moi")
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
        message=Message(trame.id_or,trame.id_mes)
        q.put(message)

    print("Trame processée!")
    return (trame.id_or,trame.id_mes) #pour débug 


# réception : à mettre dans le main pour tester en conditions réelles  
def reception(q):
    reception = subprocess.Popen(["candump","any"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    while True: 
        output=reception.stdout.readline()
        if output:
            process_mess(output.strip(),q) #output.strip() est un string 

def main(q): 
    test_reception(q)
    
