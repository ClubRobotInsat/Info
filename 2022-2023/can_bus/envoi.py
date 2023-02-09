from utiles import tab_ids
from time import sleep
from threading import Event
from utiles import dict_events

############################### initialisation du can ##################################
import can

bus = can.Bus(interface='socketcan',
              channel='can0',
              receive_own_messages=True)


##########################################################################################


# le message passé est le message que l'on ATTEND (attention à l'ordre de id_dest et id_or)
def attendre_confirmation(prio, id_dest, id_or, data):
    event = Event()
    dict_events[(prio,id_dest,id_or,data)]=event
    # print(dict_events[(prio,id_dest,id_or,data)])
    event.wait() # visiblement le set ne marche pas, on reste bloqué là 
    


def construire_en_tete(prio, id_dest, id_or):
    return (prio << 8) + (id_dest << 4) + id_or


# prio int, id_dest int, id_or int, data string (pour l'instant)
def envoyer(prio, id_dest, id_or, data):  # TODO : gérer correspondance actions / bytes
    en_tete = construire_en_tete(prio, id_dest, id_or)
    # check raise ValueError si pb ?
    # arbitration_id est un int!!
    # is_extended_id=False car id de 11 bits
    # data est un tableau d'octets!!
    message = can.Message(check=True, arbitration_id=en_tete, is_extended_id=False,
                          data=bytearray(data, encoding="utf-8"))
    sent = False
    timeout = 0.015
    while not sent:

        try:
            bus.send(message, timeout=0.2)  # en l'état valeur par défaut pour timeout
            sent = True  # TODO : est-ce que ce timeout doit être changé?
        except can.CanOperationError as e:
            sleep(timeout)  # TODO : trouver une valeur cohérente?
            # j'ai envoyé 100000 messages dans un for et les 100000 sont arrivés
            timeout = (timeout + 0.015) % 0.1
            print(e, "je retente d'envoyer le message")
            bus.send(message, timeout=0.2)


