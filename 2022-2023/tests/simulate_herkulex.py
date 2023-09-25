import can
import sys
sys.path.append('/home/pi/Info/2022-2023/can_bus')
from manager import recevoir
from manager import decomposer_en_tete,envoyer


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
        break 
