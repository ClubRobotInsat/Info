import subprocess


class Trame(object):

    def __init__(self,mess):
        self.id_dest = int(mess[0])>>4
        self.id_or = int(mess[0])&15 
        self.id_mes = int(mess[1])>>5
        self.seq = (int(mess[1])>>1)&15
        self.ack = int(mess[1])&1   # TODO : process les ack 
        self.data = mess[2:]


class Message(object): 
    def __init__(self,id_or,id_mes):
        self.id_or=id_or
        self.id_mes=id_mes
        self.data=[]
        for trame in buffer[(id_or,id_mes)]:
            self.data.extend(trame.data)



id_raspi = 0 

# nb de stm/raspi connectés
nb_disp=16
# nb de messages différents pouvant être envoyés en simultané par le même dispositif
nb_mess=8
# nb de trames max par message 
nb_trames = 16 
keys = [(id_or,id_mes) for id_or in range(nb_disp) for id_mes in range(nb_mess)]

# dictionnaire avec key = (id_or,id_mes) 
buffer = {key:[] for key in keys}


# pour tester 
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


def process_mess(trame,buffer):
    print("process Trame...")
    #récupérer les différents champs de l'en-tête dans des variables
    trame=trame.split(" ") ## TODO adapter au format des trames reçus par le candump, 
    # et peut-être aussi vérifier que le format du string reçu est le bon  
    trame=Trame(trame)
    #si le Trame est pas pour moi return 
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
    # TODO : mettre le message dans la queue si il est terminé 
    # message reçu en entier : 
    # dernière trame reçue (seq == 0) et toutes les trames sont là 
    if ((ligne_buff[-1].seq==0) and (len(ligne_buff)==ligne_buff[0].seq+1)): 
        message=Message(trame.id_or,trame.id_mes)
    print("Trame processée!")
    return (trame.id_or,trame.id_mes) #pour débug 

def test_reception(): 
    print("--------------------------------test de la réception------------------------------------")

    # 0100 0001 001 0010 0 
    print("appel de process mess avec en tête 4 1 1 2 0")
    process_mess("65 36 hola tu",buffer)
    print("\n")

    # 0000 0001 001 0010 0
    print("appel de process mess avec en tête 0 1 1 2 0")
    process_mess("1 36 hola tu",buffer)
    print("\n")

    print("test de la mise dans le buffer")
    print("data envoyée dans le désordre: hola tu que tal kfjdjk")
    print("\n")
    
    # 0000 0001 001 0000 0 
    (id_or,id_mes) = process_mess("1 32 kfjdjk",buffer)
    print("\n")

    # 0000 0001 001 0001 0 
    process_mess("1 34 que tal",buffer)
    print("\n")
    # print_ligne_buff(id_or,id_mes)
    print("--------------------------------------------------------------------------------------------")

# réception : à mettre dans le main pour tester en conditions réelles  
def reception():
    reception = subprocess.Popen(["candump","any"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    while True: 
        output=reception.stdout.readline()
        if output:
            process_mess(output.strip(),buffer) #output.strip() est un string 

def main(): 
    test_reception()