import subprocess


class Message(object):

    def __init__(self,mess):
        self.id_dest = int(mess[0])>>4
        self.id_or = int(mess[0])&15 
        self.id_mes = int(mess[1])>>5
        self.seq = (int(mess[1])>>1)&15
        self.ack = int(mess[1])&1   
        self.data = mess[2:]
    


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
    for txt in buffer[(id_or,id_mes)]:
        if txt != None : 
            print(txt)

def test_variables(id_dest,id_or,id_mes,seq,ack): 
    print("variables récupérées :")
    print("id_dest =",id_dest)
    print("id_or =",id_or)
    print("id_mes =",id_mes)
    print("seq =",seq)
    print("ack =",ack)


def process_mess(mess,buffer):
    print("process message...")
    #récupérer les différents champs de l'en-tête dans des variables
    mess=mess.split(" ") ## TODO adapter au format des messages reçus par le candump, 
    # et peut-être aussi vérifier que le format du string reçu est le bon  
    mess=Message(mess)
    #si le message est pas pour moi return 
    if mess.id_dest != id_raspi:
        print("ce message n'est pas pour moi")
        return 
    #si le message est pour moi, traiter et mettre dans buffer  
    # test_variables(id_dest,id_or,id_mes,seq,ack)
    # TODO : append dans l'ordre même si les messages ne sont pas envoyés dans l'ordre 
    buffer[(mess.id_or,mess.id_mes)].append(mess.data)
    # TODO : mettre le message dans la queue si il est terminé 
    print("message processé!")
    return (mess.id_or,mess.id_mes)

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
    print_ligne_buff(id_or,id_mes)
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