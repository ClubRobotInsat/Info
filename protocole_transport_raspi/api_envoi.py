import subprocess

import utiles
from utiles import Message, Trame
from utiles import nb_trames as trames_max
from utiles import size_payload
from utiles import buffer_acks
from math import ceil
from multiprocessing import Condition, Lock

# timeout pour la réception des acks
timeout = 3


def test_envoi(ack_received, lock_buffer_acks):
    envoyer(Message(3, 0,
                        ['FF', 'EE', 'AA', 'AA', 'CC', 'BB', '01', '01', '01', '01', '01', 'CC', '01', '01', '01', '01',
                         '01', '01', '01']), ack_received, lock_buffer_acks)

    # TODO : more tests
    envoyer(Message(9, 0, ['00']), ack_received, lock_buffer_acks)
    envoyer(Message(88, 0, ['']), ack_received, lock_buffer_acks)
    envoyer(Message(9, 9, ['']), ack_received, lock_buffer_acks)
    envoyer(Message(1, 0, "ksjhflsdkfghsldfvb"), ack_received, lock_buffer_acks)
    print("envoi d'un message à la raspi")
    envoyer(Message(0,0, ['AA']), ack_received, lock_buffer_acks)


def envoyer(message, ack_received, lock_buffer_envoi):
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
    lock_buffer_envoi.acquire()
    buffer_acks[message.id_dest, message.id_mes] = seq
    print("buffer acks : ", buffer_acks[message.id_dest, message.id_mes])
    lock_buffer_envoi.release()
    while to_send:
        trame = Trame((message.id_dest, message.id_mes, seq))
        trame.data = to_send[:size_payload]
        to_send = to_send[size_payload:]
        # remplir la trame de 0 si elle fait pas 8 octets
        if len(trame.data) < utiles.size_payload:
            trame.data.extend(['00' for _ in range(utiles.size_payload-len(trame.data))])
        # send trame 
        str_trame = trame.to_string()
        # subprocess.Popen(["cansend", "can0", str_trame], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        #                stderr=subprocess.PIPE)
        print(str_trame)
        seq -= 1
    # wait avec un timeout
    ack_received.acquire()
    if ack_received.wait(timeout):
        print("message envoyé!")
        print("#######################message envoyé dans sa totalité######################")
    else:
        print("échec de l'envoi du message, timeout expiré")


def process_ack(trame, ack_received, lock_buffer_envoi):
    print("process ack...")
    lock_buffer_envoi.acquire()
    print("buffer acks : ", buffer_acks[trame.id_dest, trame.id_mes])
    buffer_acks[trame.id_or, trame.id_mes] -= 1
    # on a reçu tous les acks
    if buffer_acks[trame.id_or, trame.id_mes] == 0:
        ack_received.acquire()
        ack_received.notify_all()
    print("ligne buff : ", buffer_acks[trame.id_or, trame.id_mes])
    lock_buffer_envoi.release()

