from can_bus import envoi 
from can_bus import reception 

# TODO test : lancer simulate_herkulex puis ce programme et vérifier si ça marche 
async def bouger_bras(mouvement):
    envoi.envoyer(2,2,1,mouvement)
    envoi.attendre_confirmation(2,1,2,mouvement)