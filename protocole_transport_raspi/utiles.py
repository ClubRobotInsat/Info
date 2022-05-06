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

# nb de stm/raspi connectés
nb_disp=16
# nb de messages différents pouvant être envoyés en simultané par le même dispositif
nb_mess=8
# nb de trames max par message 
nb_trames = 16 
keys = [(id_or,id_mes) for id_or in range(nb_disp) for id_mes in range(nb_mess)]

# dictionnaire avec key = (id_or,id_mes) 
buffer = {key:[] for key in keys}
