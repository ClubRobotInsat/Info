class Trame(object):

    mes_counter = 0

    def __init__(self, arg):
        # pour créer une trame à envoyer depuis l'api d'envoi
        if isinstance(arg, int):
            self.id_dest = arg
            self.id_or = id_raspi
            self.id_mes = Trame.mes_counter
            Trame.mes_counter = (Trame.mes_counter+1) % nb_mess
            self.seq = 0  # TODO : implémenter pour +ieurs trames / message
            self.ack = 0
            self.data = []

        else:  # pour créer une trame depuis la réception à partir du message reçu par bash
            # passer des strings à des int (et il prend en compte que c'est de l'hexa avec le 16)
            self.id_dest = int(arg[0], 16) >> 4
            self.id_or = int(arg[0], 16) & 15
            self.id_mes = int(arg[1], 16) >> 5
            self.seq = (int(arg[1], 16) >> 1) & 15
            self.ack = int(arg[1], 16) & 1  # TODO : process les ack
            self.data = arg[2:]
            # ATTENTION la data est sous forme de liste de strings

    def to_string(self):
        # bytes d'en tête
        trame_bytes = [hex(self.id_dest << 4 | self.id_or), hex(self.id_mes << 5 | self.seq << 1 | self.ack)]
        # bytes de data
        for d in self.data:
            trame_bytes.append(d)
        trame_str = ""
        for byte in trame_bytes:
            trame_str += str(byte)
            trame_str += " "
        trame_str = trame_str.replace("0x", "")
        return trame_str


class Message(object):
    def __init__(self, id_dest, id_or, id_mes, data=None):
        if data is None:
            data = []
        self.id_dest = id_dest
        self.id_or = id_or
        self.id_mes = id_mes
        self.data = data
        if (id_or, id_mes) == (-1, -1):  # permet de créer un message vide
            return
        for trame in buffer_reception[(id_or, id_mes)]:
            self.data.extend(trame.data)


id_raspi = 0

# nb d'octets de data par trame 
size_payload = 6
# nb de stm/raspi connectés
nb_disp = 16
# nb de messages différents pouvant être envoyés en simultané par le même dispositif
nb_mess = 8
# nb de trames max par message 
nb_trames = 16

# dictionnaire avec key = (id_or,id_mes)
keys = [(id_or, id_mes) for id_or in range(nb_disp) for id_mes in range(nb_mess)]
buffer_reception = {key: [] for key in keys}

