from utiles import Message, Trame
import subprocess
from utiles import nb_trames as trames_max
from utiles import size_payload


def envoyer(id_dest, data):
    size_data = len(data)
    nb_trames = size_data / size_payload
    acks = [0 for i in range(nb_trames)]
    if nb_trames > trames_max:
        print("ce message est trop long pour être envoyé")
        return
    to_send = data
    trame = Trame(id_dest)
    while to_send:
        trame.data = +to_send[:size_payload - 1]
        to_send = to_send[size_payload - 1:]
        # send trame 
        str_trame = trame.to_string()
        envoi = subprocess.Popen(["cansend", "can0", str_trame], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        # cansend can0 <id>#{data}
    # reduce pour vérifier que tous les ack ont été reçus 
    print("message envoyé!")


# TODO : implémenter pour des messages de plus d'un trame
def process_ack(q_envoi):
    while (1):
        trame = q_envoi.get()
        # comment dire à envoyer que l'ack a bien été reçu?
