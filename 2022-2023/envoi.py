from utiles import tab_ids
from time import sleep

############################### initialisation du can ##################################
import can

bus = can.Bus(interface='socketcan',
              channel='can0',
              receive_own_messages=True)

##########################################################################################



def construire_en_tete(prio, id_dest, id_or):
    return (prio << 8) + (id_dest << 4) + id_or

# prio int, dest string, data string (pour l'instant) 
def envoyer(prio, dest, data): # TODO : gérer correspondance actions / bytes
    id_dest=tab_ids[dest]
    id_or=tab_ids["raspi"]
    en_tete=construire_en_tete(prio, id_dest, id_or)
    # check raise ValueError si pb ?
    # arbitration_id est un int!!
    # is_extended_id=False car id de 11 bits
    # data est un tableau d'octets!!
    message=can.Message(check=True, arbitration_id=en_tete, is_extended_id=False, data=bytearray(data, encoding="utf-8"))
    try :
        bus.send(message, timeout=0.2)# en l'état valeur par défaut pour timeout
                                        # TODO : est-ce que ce timeout doit être changé?
    except can.CanOperationError:
        sleep(1) #TODO : trouver une valeur cohérente
        print(can.CanOperationError + "je retente d'envoyer le message")
        bus.send(message, timeout=0.2)

    # TODO : attendre la confirmation que tout s'est bien passé




