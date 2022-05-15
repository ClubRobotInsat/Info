import subprocess

import utiles
from utiles import Message, Trame
from utiles import nb_trames as trames_max
from utiles import size_payload
from utiles import buffer_acks
from math import ceil


def test_envoi():
    for i in range(10):
        envoyer(Message(3, 0,
                        ['FF', 'EE', 'AA', 'AA', 'CC', 'BB', '01', '01', '01', '01', '01', 'CC', '01', '01', '01', '01',
                         '01', '01', '01']))

    # TODO : more tests
    envoyer(Message(9, 0, ['00']))
    envoyer(Message(88,0,['']))
    envoyer(Message(9,9,['']))
    envoyer(Message(1,0,"ksjhflsdkfghsldfvb"))

def envoyer(message):

    if message.id_dest < 0 or message.id_dest > utiles.nb_disp:
        print("ce destinataire n'existe pas")
        return

    if message.id_or is not utiles.id_raspi:
        print("vous ne pouvez pas envoyer un message avec une autre id que celle de la raspi")
        return

    size_data = len(message.data)
    nb_trames = ceil(size_data / size_payload)

    if nb_trames > trames_max:
        print("ce message est trop long pour être envoyé")
        return

    to_send = message.data
    seq = nb_trames - 1
    while to_send:
        trame = Trame((message.id_dest, message.id_mes, seq))
        trame.data = to_send[:size_payload]
        to_send = to_send[size_payload:]
        # send trame 
        str_trame = trame.to_string()
        #subprocess.Popen(["cansend", "can0", str_trame], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
         #                stderr=subprocess.PIPE)
        print(str_trame)
        seq -= 1
    # wait avec un timeout
    print("message envoyé!")


def process_ack(trame, ack_received):
    print("process ack...")
    # reduce pour vérifier que tous les ack ont été reçus
    ligne_buff = buffer_acks[trame.id_or, trame.id_mes]
    ligne_buff.append(trame.seq)
    # si on a reçu le premier et le
    print(ligne_buff)

