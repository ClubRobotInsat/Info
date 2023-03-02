############################### initialisation du can ##################################
import can

bus = can.Bus(interface='socketcan',
              channel='can0',
              receive_own_messages=True)


##########################################################################################


# id en décimal

tab_ids={"raspi":1, "herkulex":2, "base roulante":3}

reversed_tab_ids=dict((v,k) for (k,v) in tab_ids.items())

# TODO : chaque objet doit avoir une méthode to_bytes() pour passer les commandes / arguments à bytes

dict_events={} ## ne JAMAIS itérer là-dessus car accès concurrents 
# key : tuple(prio,id_dest,id_or,data) value : event      

