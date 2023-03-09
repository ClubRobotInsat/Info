from __init__ import bus,reversed_tab_ids,dict_events
from time import sleep
#from time import Event
from threading import Event
import can

def decomposer_en_tete(en_tete: int):
    return en_tete >> 8, (en_tete >> 4) & 15, en_tete & 15

def construire_en_tete(prio, id_dest, id_or):
    return (prio << 8) + (id_dest << 4) + id_or


# le message passé est le message que l'on ATTEND (attention à l'ordre de id_dest et id_or)
def attendre_confirmation(prio, id_dest, id_or, data):
    event = Event()
    dict_events[(prio,id_dest,id_or,data)]=event
    # print(dict_events[(prio,id_dest,id_or,data)])
    event.wait() # visiblement le set ne marche pas, on reste bloqué là 
    


def recevoir():
    for msg in bus:
        (prio, id_dest, id_or) = decomposer_en_tete(msg.arbitration_id)
        if (id_dest==1):
            data = msg.data.decode() # c'est un string 
            print(prio)
            print(id_or)
            print(data)
            print("message reçu de " + reversed_tab_ids[id_or] + " : " + msg.data.decode() + " à destination de " + reversed_tab_ids[id_dest])
            try:
                event = dict_events[(prio,id_dest,id_or,data)]
                print("confirmation reçue")
                event.set()
            except:
                print("bruh")
                
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



