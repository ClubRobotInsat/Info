from utiles import tab_noms

############################### initialisation du can ##################################
import can

bus = can.Bus(interface='socketcan',
              channel='can0',
              receive_own_messages=True)

##########################################################################################

# l'en tête est un int
def decomposer_en_tete(en_tete):
    return (en_tete>>8,(en_tete>>4)&15,en_tete&15)




for msg in bus:
    (prio, id_dest, id_or) = decomposer_en_tete(msg.arbitration_id)
    print("message reçu de " + tab_noms[id_or] + " : " + msg.data.decode() + " à destination de " + tab_noms[id_or])