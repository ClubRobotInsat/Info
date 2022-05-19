class Trame(object):

    def __init__(self, arg, ack=0):
        # pour créer une trame à envoyer depuis l'api d'envoi
        if isinstance(arg, tuple):
            self.id_dest = arg[0]
            self.id_or = id_raspi
            self.id_mes = arg[1]
            self.seq = arg[2]
            self.ack = ack
            self.data = ['00' for i in range(size_payload)]

        else:  # pour créer une trame depuis la réception à partir du message reçu par bash
            # passer des strings à des int (et il prend en compte que c'est de l'hexa avec le 16)
            # print(arg)
            self.id_dest = int(arg[0], 16) >> 4
            self.id_or = int(arg[0], 16) & 15
            self.id_mes = int(arg[1], 16) >> 5
            self.seq = (int(arg[1], 16) >> 1) & 15
            self.ack = int(arg[1], 16) & 1
            self.data = arg[2:]
            # ATTENTION la data est sous forme de liste de strings

    def to_string(self):
        # bytes d'en tête
        trame_bytes = [hex(self.id_dest << 4 | self.id_or), hex(self.id_mes << 5 | self.seq << 1 | self.ack)]
        # bytes de data
        for d in self.data:
            trame_bytes.append(d)
        trame_str = "000#"  # un truc du cansend, je sais pas vraiment à quoi ça sert
        for byte in trame_bytes:
            trame_str += str(byte)
            trame_str += " "
        trame_str = trame_str.replace("0x", "")
        return trame_str


class Message(object):
    mes_counter = 0

    def __init__(self, id_dest, id_or, data):
        self.data = data
        self.id_dest = id_dest
        self.id_or = id_or
        self.id_mes = Message.mes_counter
        Message.mes_counter = (Message.mes_counter + 1) % nb_mess


id_raspi = 0

# nb d'octets de data par trame 
size_payload = 6
# nb de stm/raspi connectés
nb_disp = 16
# nb de messages différents pouvant être envoyés en simultané par le même dispositif
nb_mess = 8
# nb de trames max par message 
nb_trames = 16

# dictionnaire avec keys = (id_or,id_mes)
keys = [(id_or, id_mes) for id_or in range(nb_disp) for id_mes in range(nb_mess)]

# buffer où la réception met les trames en attendant que le message soit reçu au complet
buffer_reception = {key: [] for key in keys}

# buffer où l'envoi met les acks reçus
# chaque ligne du buffer contient le nb de trames du message, décrémenté à chaque réception de ack
buffer_acks = {key: -1 for key in keys}
