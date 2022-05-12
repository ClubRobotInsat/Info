class Trame(object):

    def __init__(self,arg):
        # pour créer une trame depuis la réception à partir du message reçu par bash 
        if isinstance(arg,list):
            self.id_dest = (int(arg[0],16))>>4 # passer des string à des int (et il prend en compte que c'est de l'hexa avec le 16)
            self.id_or = int(arg[0],16)&15 
            self.id_mes = int(arg[1],16)>>5
            self.seq = (int(arg[1],16)>>1)&15
            self.ack = int(arg[1],16)&1   # TODO : process les ack 
            self.data = arg[2:]
        # pour créer une trame à envoyer depuis l'api d'envoi 
        elif isinstance(arg,int):
            self.id_dest=arg
            self.id_or=id_raspi
            self.id_mes=0 # TODO : faire une variable statique pour éviter les redondances 
            self.seq=0 # TODO : implémenter pour +ieurs trames / message 
            self.ack=0
            self.data= []



class Message(object): 
    def __init__(self,id_dest,id_or,id_mes,data=[]):
        self.id_dest=id_dest
        self.id_or=id_or
        self.id_mes=id_mes
        self.data=data
        if (id_or,id_mes)==(-1,-1): # permet de créer un message vide 
            return
        for trame in buffer[(id_or,id_mes)]:
            self.data.extend(trame.data)


# nb d'octets de data par trame 
size_payload=6
# nb de stm/raspi connectés
nb_disp=16
# nb de messages différents pouvant être envoyés en simultané par le même dispositif
nb_mess=8
# nb de trames max par message 
nb_trames = 16 
keys = [(id_or,id_mes) for id_or in range(nb_disp) for id_mes in range(nb_mess)]

id_raspi = 0 


# dictionnaire avec key = (id_or,id_mes) 
buffer = {key:[] for key in keys}
