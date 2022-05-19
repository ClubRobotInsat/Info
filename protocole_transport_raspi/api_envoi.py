import subprocess

import utiles
from utiles import Message, Trame
from utiles import nb_trames as trames_max
from utiles import size_payload
from utiles import buffer_acks
from math import ceil
from api_reception import process_mess

# timeout pour la réception des acks
timeout = 30  # TODO : valeur cohérente


def test_envoi(ack_received, lock_buffer_acks, buffer_acks):
    envoyer(Message(3, 0,
                    ['FF', 'EE', 'AA', 'AA', 'CC', 'BB', '01', '01', '01', '01', '01', 'CC', '01', '01', '01', '01',
                     '01', '01', '01']))

    # TODO : more tests
    # envoyer(Message(9, 0, ['00']), ack_received, lock_buffer_acks)
    # envoyer(Message(88, 0, ['']), ack_received, lock_buffer_acks)
    # envoyer(Message(9, 9, ['']), ack_received, lock_buffer_acks)
    # envoyer(Message(1, 0, "ksjhflsdkfghsldfvb"), ack_received, lock_buffer_acks)
    # print("envoi d'un message à la raspi")
    # envoyer(Message(0,0, ['AA']), ack_received, lock_buffer_acks)


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
    buffer_acks[message.id_dest, message.id_mes] = seq
    print("buffer acks : ", buffer_acks[message.id_dest, message.id_mes])
    while to_send:
        trame = Trame((message.id_dest, message.id_mes, seq))
        trame.data = to_send[:size_payload]
        to_send = to_send[size_payload:]
        # remplir la trame de 0 si elle fait pas 8 octets
        if len(trame.data) < utiles.size_payload:
            trame.data.extend(['00' for _ in range(utiles.size_payload - len(trame.data))])
        # send trame 
        str_trame = trame.to_string()
        # subprocess.Popen(["cansend", "can0", str_trame], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        #                stderr=subprocess.PIPE)
        print(str_trame)
        print("seq : ", seq)
        seq -= 1
    # idée moche mais peut marcher : se mettre en réception ici au lieu d'attendre les acks d'un autre process
    # edit : marchera pas car si je mets plusieurs bash en réception ça va forcément merder 
    assenti = False
    reception_bash = subprocess.Popen(["candump", "any"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
    while not assenti:
        output = reception_bash.stdout.readline()
        if output:
            print("process ack...")

        trame = trame.split(" ")
        trame = Trame(trame[3:])  # trame [3:] pour virer l'en tête du candump

        # si la trame est pas pour moi return
        if trame.id_dest != utiles.id_raspi:
            print("ce message n'est pas pour moi")
            return

        if trame.ack == 1:
            print("ack reçu, process_ack")
            print("process ack...")
            print("buffer acks : ", buffer_acks[trame.id_or, trame.id_mes])
            buffer_acks[trame.id_or, trame.id_mes] -= 1
            # on a reçu tous les acks
            if buffer_acks[trame.id_or, trame.id_mes] == 0:
                assenti = True
                print("on a bien reçu les acks")
            print("ligne buff : ", buffer_acks[trame.id_or, trame.id_mes])

    return

    # wait avec un timeout
    # ack_received.acquire()
    # if ack_received.wait(timeout):
    #   print("message envoyé!")
    #  print("#######################message envoyé dans sa totalité######################")
    # else:
    #   print("échec de l'envoi du message, timeout expiré")


def process_ack(trame, ack_received, lock_buffer_envoi, buffer_acks):
    print("process ack...")
    lock_buffer_envoi.acquire(True)
    print("buffer acks : ", buffer_acks[trame.id_or, trame.id_mes])
    buffer_acks[trame.id_or, trame.id_mes] -= 1
    # on a reçu tous les acks
    if buffer_acks[trame.id_or, trame.id_mes] == 0:
        ack_received.acquire()
        ack_received.notify_all()
    print("ligne buff : ", buffer_acks[trame.id_or, trame.id_mes])
    lock_buffer_envoi.release()
