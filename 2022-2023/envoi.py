from utiles import tab_ids


############################### initialisation du can ##################################
import can

bus = can.Bus(interface='socketcan',
              channel='can0',
              receive_own_messages=True)

##########################################################################################



def construire_en_tete(prio, id_dest, id_or):
    return (prio << 8) + (id_dest << 4) + id_or

def envoyer(prio, dest, str_data): # TODO : tableau avec les actions à effectuer et une correspondance en bytes direct
    id_dest=tab_ids[dest]
    id_or=tab_ids["raspi"]
    en_tete=construire_en_tete(prio, id_dest, id_or)
    # check raise ValueError si pb ?
    # arbitration_id est un int!!
    # is_extended_id=False car id de 11 bits
    # data est un tableau d'octets!!
    message=can.Message(check=True, arbitration_id=en_tete, is_extended_id=False, data=bytearray(str_data,encoding="utf-8"))
    bus.send(message, timeout=0.2)
    # en l'état valeur par défaut pour timeout
    # TODO : est-ce que ce timeout doit être changé?

    # TODO : attendre la confirmation que tout s'est bien passé




