import subprocess

import utiles
from utiles import Message, Trame
from utiles import nb_trames as trames_max
from utiles import size_payload
from utiles import buffer_acks
from math import ceil
from multiprocessing import Condition

# timeout pour la réception des acks
timeout = 3


def test_envoi(ack_received):
    envoyer(Message(3, 0,
                        ['FF', 'EE', 'AA', 'AA', 'CC', 'BB', '01', '01', '01', '01', '01', 'CC', '01', '01', '01', '01',
                         '01', '01', '01']), ack_received)

    # TODO : more tests
    envoyer(Message(9, 0, ['00']), ack_received)
    envoyer(Message(88, 0, ['']), ack_received)
    envoyer(Message(9, 9, ['']), ack_received)
    envoyer(Message(1, 0, "ksjhflsdkfghsldfvb"), ack_received)


def envoyer(message, ack_received):
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
    buffer_acks[message.id_dest, message.id_mes] = seq
    while to_send:
        trame = Trame((message.id_dest, message.id_mes, seq))
        trame.data = to_send[:size_payload]
        to_send = to_send[size_payload:]
        # send trame 
        str_trame = trame.to_string()
        # subprocess.Popen(["cansend", "can0", str_trame], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        #                stderr=subprocess.PIPE)
        # print(str_trame)
        seq -= 1
    # wait avec un timeout
    ack_received.acquire()
    if ack_received.wait(timeout):
        print("message envoyé!")
        print("#######################message envoyé dans sa totalité######################")
    else:
        print("échec de l'envoi du message, timeout expiré")


def process_ack(trame, ack_received):
    print("process ack...")
    buffer_acks[trame.id_or, trame.id_mes] -= 1
    ligne_buff = buffer_acks[trame.id_or, trame.id_mes]
    # on a reçu tous les acks
    if ligne_buff == 0:
        ack_received.acquire()
        ack_received.notify_all()
    print(ligne_buff)
