import can
from envoi import envoyer
from reception import decomposer_en_tete

bus = can.Bus(interface='socketcan',
              channel='can0',
              receive_own_messages=True)


for msg in bus:
    (prio, id_dest, id_or) = decomposer_en_tete(msg.arbitration_id)

    if (id_dest==2):    
        data=msg.data.decode("utf-8")
        print("j'ai reçu " + data)
        envoyer(prio,id_or,id_dest,data)
        print("confirmation envoyée")
