# id en décimal

tab_ids={"raspi":1, "herkulex":2, "base roulante":3}

reversed_tab_ids=dict((v,k) for (k,v) in tab_ids.items())

# TODO : chaque objet doit avoir une méthode to_bytes() pour passer les commandes / arguments à bytes