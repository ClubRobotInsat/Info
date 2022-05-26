import subprocess
from utiles import Trame, Message
from utiles import buffer_reception
from utiles import id_raspi
from time import sleep


# pour tester
###############################################################################################################

def print_ligne_buff(id_or, id_mes):
    print("(", id_or, ",", id_mes, ") : ")
    for mess in buffer_reception[(id_or, id_mes)]:
        if mess is not None:
            print(mess.data)


def test_variables(trame):
    print("variables récupérées :")
    print("id_dest =", trame.id_dest)
    print("id_or =", trame.id_or)
    print("id_mes =", trame.id_mes)
    print("seq =", trame.seq)
    print("ack =", trame.ack)


def test_reception(q, buffer_acks, ack_received_cond):
    print("--------------------------------test de la réception------------------------------------")

    # 0100 0001 001 0000 0
    print("appel de process mess avec en tête 4 1 1 0 0")
    process_mess("can0 001 [8] 41 20 01 01 01 01 01 01", q, buffer_acks, ack_received_cond)
    print("\n")

    # 0000 0001 001 0010 0
    print("appel de process mess avec en tête 0 1 1 2 0")
    process_mess("can0 001 [8] 01 24 FF EE AA AA CC BB", q, buffer_acks, ack_received_cond)
    print("\n")

    # 0000 0001 001 0000 0
    print("appel de process mess avec en tête 0 1 1 0 0")

    process_mess("can0 001 [8] 01 20 01 01 01 01 01 01", q, buffer_acks, ack_received_cond)
    print("\n")

    # 0000 0001 001 0001 0 
    print("appel de process mess avec en tête 0 1 1 1 0")

    process_mess("can0 001 [8] 01 22 01 01 01 01 01 01", q, buffer_acks, ack_received_cond)
    print("\n")

    # 1111 1000 111 1100 1 
    print("appel de process mess avec en tête 15 8 7 12 1")
    process_mess("can0 001 [8] F8 F9 01 01 01 01 01 01", q, buffer_acks, ack_received_cond)
    print("\n")

    sleep(1)
    # TODO : more tests
    # tests des acks :
    # 0000 0011 000 0010 1
    print("appel de process mess avec en tête 0 3 0 2 1")
    process_mess("can0 001 [8] 03 05 01 01 01 01 01 01", q, buffer_acks, ack_received_cond)
    print("\n")

    # 0000 0011 000 0011 1
    print("appel de process mess avec en tête 0 3 0 3 1")
    process_mess("can0 001 [8] 03 07 01 01 01 01 01 01", q, buffer_acks, ack_received_cond)
    print("\n")

    # 0000 0011 000 0000 1
    print("appel de process mess avec en tête 0 3 0 0 1")
    process_mess("can0 001 [8] 03 01 01 01 01 01 01 01", q, buffer_acks, ack_received_cond)
    print("\n")

    # 0000 0011 000 0001 1
    print("appel de process mess avec en tête 0 3 0 1 1")
    process_mess("can0 001 [8] 03 03 01 01 01 01 01 01", q, buffer_acks, ack_received_cond)
    print("\n")

    print("--------------------------------------------------------------------------------------------")


###############################################################################################################


def process_mess(trame, q, buffer_acks, ack_received_cond, buffer_lock):
    trame = trame.split(" ")
    trame = Trame(trame[7:])  # trame [7:] pour virer l'en tête du candump

    # si la trame est pas pour moi return
    if trame.id_dest != id_raspi:
        print("ce message n'est pas pour moi")
        return

    # si le message est un ack, on le processe comme tel
    if trame.ack == 1:
        buffer_lock.acquire()
        if buffer_acks[trame.id_or, trame.id_mes] != -1: # ce ack nous concerne
            buffer_acks[trame.id_or, trame.id_mes] -= 1
        # on a reçu tous les acks, on notifie l'envoi
        if buffer_acks[trame.id_or, trame.id_mes] == 0:
            ack_received_cond.acquire()
            ack_received_cond.notify_all()
            ack_received_cond.release()
            # reset la ligne du buffer à -1 pour qu'on soit sache qu'il n'y a plus de message en attente de confirmation
            buffer_acks[trame.id_or, trame.id_mes] = -1
        buffer_lock.release()
        return

    # si le message est pour moi, traiter et mettre dans buffer
    ligne_buff = buffer_reception[(trame.id_or, trame.id_mes)]
    # append dans le buffer dans l'ordre
    if not ligne_buff:
        ligne_buff.append(trame)
    elif ligne_buff[-1].seq == trame.seq:
        print("t'as reçu le même message plusieurs fois")
    elif ligne_buff[-1].seq < trame.seq: # TODO : première cond rajoutée pendant la coupe à l'arrache
        dernier = ligne_buff[-1]
        ligne_buff[-1] = trame
        ligne_buff.append(dernier)
    else:
        ligne_buff.append(trame)

    # envoyer ack de la trame
    trame_ack = Trame((trame.id_or, trame.id_mes, trame.seq), ack=1)
    str_trame_ack = trame_ack.to_string()
    print("ack envoyé : ", str_trame_ack)
    # TODO : uncomment to test
    envoi_ack = subprocess.Popen(["cansend", "can0", str_trame_ack], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    # print(envoi_ack.stderr.read())
    # message reçu en entier :
    # dernière trame reçue (seq == 0) et toutes les trames sont là 
    if (ligne_buff[-1].seq == 0) and (len(ligne_buff) == ligne_buff[0].seq + 1):
        data = []  # data du message
        for trame in buffer_reception[(trame.id_or, trame.id_mes)]:
            data.extend(trame.data)
        message = Message(trame.id_dest, trame.id_or, data)
        q.put(message)
        buffer_reception[(trame.id_or, trame.id_mes)] = []



def reception(q, buffer_acks, ack_received_cond, buffer_lock):
    reception_bash = subprocess.Popen(["candump", "any"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
    while True:
        output = reception_bash.stdout.readline()
        if output:
            print("reçu au can : ", output.strip().decode())
            process_mess(output.strip().decode(), q, buffer_acks, ack_received_cond, buffer_lock)  # output.strip().decode() est un string
