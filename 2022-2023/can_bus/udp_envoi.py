import can
from time import sleep

def init():
    bus = can.Bus(interface='socketcan',
                  channel='can0',
                  receive_own_messages=True)

    return bus


def construire_message(en_tete, data):
    message = can.Message(check=True, arbitration_id=en_tete, is_extended_id=False,
                          data=bytearray(data, encoding="utf-8"))
    return message


def envoyer(message, bus):
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

