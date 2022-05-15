import subprocess
from utiles import Trame, Message
from utiles import buffer_reception
from utiles import id_raspi
from api_envoi import process_ack


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


def test_reception(q, ack_received):
    print("--------------------------------test de la réception------------------------------------")

    # 0100 0001 001 0010 0 
    print("appel de process mess avec en tête 4 1 1 2 0")
    process_mess("can0 001 [8] 41 24 01 01 01 01 01 01", q, ack_received)
    print("\n")

    # 0000 0001 001 0010 0
    print("appel de process mess avec en tête 0 1 1 2 0")
    process_mess("can0 001 [8] 01 24 FF EE AA AA CC BB", q, ack_received)
    print("\n")

    # 0000 0001 001 0000 0
    print("appel de process mess avec en tête 0 1 1 0 0")

    process_mess("can0 001 [8] 01 20 01 01 01 01 01 01", q, ack_received)
    print("\n")

    # 0000 0001 001 0001 0 
    print("appel de process mess avec en tête 0 1 1 1 0")

    process_mess("can0 001 [8] 01 22 01 01 01 01 01 01", q, ack_received)
    print("\n")

    # 1111 1000 111 1100 1 
    print("appel de process mess avec en tête 15 8 7 12 1")
    process_mess("can0 001 [8] F8 F9 01 01 01 01 01 01", q, ack_received)
    print("\n")

    # TODO : more tests
    # tests des acks :
    # 0000 0011 000 0010 1
    print("appel de process mess avec en tête 0 3 0 2 1")
    process_mess("can0 001 [8] 03 05 01 01 01 01 01 01", q, ack_received)
    print("\n")

    # 0000 0011 000 0011 1
    print("appel de process mess avec en tête 0 3 0 3 1")
    process_mess("can0 001 [8] 03 07 01 01 01 01 01 01", q, ack_received)
    print("\n")

    # 0000 0011 000 0000 1
    print("appel de process mess avec en tête 0 3 0 0 1")
    process_mess("can0 001 [8] 03 01 01 01 01 01 01 01", q, ack_received)
    print("\n")

    # 0000 0011 000 0001 1
    print("appel de process mess avec en tête 0 3 0 1 1")
    process_mess("can0 001 [8] 03 03 01 01 01 01 01 01", q, ack_received)
    print("\n")

    print("--------------------------------------------------------------------------------------------")


###############################################################################################################


# TODO : processer les ack
def process_mess(trame, q, ack_received):
    print("process Trame...")

    trame = trame.split(" ")
    trame = Trame(trame[3:])  # trame [3:] pour virer l'en tête du candump

    test_variables(trame)

    # si la trame est pas pour moi return
    if trame.id_dest != id_raspi:
        print("ce message n'est pas pour moi")
        return

    # si le message est un ack, on le passe à l'api d'envoi
    if trame.ack == 1:
        print("ack reçu, passage à process_ack")
        process_ack(trame, ack_received)
        return

    # si le message est pour moi, traiter et mettre dans buffer
    ligne_buff = buffer_reception[(trame.id_or, trame.id_mes)]
    # append dans le buffer dans l'ordre
    if not ligne_buff:
        ligne_buff.append(trame)
    elif ligne_buff[-1].seq < trame.seq:
        dernier = ligne_buff[-1]
        ligne_buff[-1] = trame
        ligne_buff.append(dernier)
    else:
        ligne_buff.append(trame)

    # message reçu en entier : 
    # dernière trame reçue (seq == 0) et toutes les trames sont là 
    if (ligne_buff[-1].seq == 0) and (len(ligne_buff) == ligne_buff[0].seq + 1):
        data = []  # data du message
        for trame in buffer_reception[(trame.id_or, trame.id_mes)]:
            data.extend(trame.data)
        message = Message(trame.id_dest, trame.id_or, data)
        q.put(message)
        print("message placé dans la file d'attente pour l'appli")

    print("Trame processée!")


def reception(q, ack_received):
    reception_bash = subprocess.Popen(["candump", "any"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
    while True:
        output = reception_bash.stdout.readline()
        if output:
            process_mess(output.strip().decode(), q, ack_received)  # output.strip() est un string
