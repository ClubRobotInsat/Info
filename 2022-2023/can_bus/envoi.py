from traitement import construire_en_tete
from utiles import tab_ids


# def set_bus_envoi():
    # TODO udp_envoi ou can_envoi, regarder comment faire


async def attendre_confirmation(confirmation_id):
    # si le message a besoin d'une confirmation, il doit venir avec une confirmation_id
    # assignée automatiquement?
    return


# prio int, dest string, data string (pour l'instant)
def envoyer(prio, dest, data, attendre_confirmation=False,
            confirmation_id=0):  # TODO : gérer correspondance actions / bytes
    id_dest = tab_ids[dest]
    id_or = tab_ids["raspi"]
    en_tete = construire_en_tete(prio, id_dest, id_or)
    # check raise ValueError si pb ?
    # arbitration_id est un int!!
    # is_extended_id=False car id de 11 bits
    # data est un tableau d'octets!!
    # TODO message à envoyer
    # TODO : tester
    sent = False
    timeout = 0.015

    ## TODO envoyer

    # if attendre_confirmation:
        # for msg in bus:
            # TODO : async en python?
          #   print("je fais des trucs")
