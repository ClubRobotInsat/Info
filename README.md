# Info
Code de haut niveau pour contrôler les actions et la stratégie du robot

2021-2022 : code de la Coupe de France 2022 

2022-2023 : code de la Coupe de France 2023 

N'hésitez pas à vous référer à la doc sur notion dans Coupe de France -> Ressources -> Raspberry Pi et Coupe de France -> Ressources -> SPI can et transreceiver

## Organisation 2022-2023 

### Lidar 
Code pour contrôler le Lidar écrit par Sébastien Vouters. 

### aruco_code 
Code pour détecter les aruco codes avec la caméra écrit par Leonardo. 

### can_bus 
Code pour utiliser le CAN bus pour envoyer et recevoir des messages depuis la raspi. Écrit par Aude Jean-Baptiste et Romain Moulin. 

**Format des messages** _IMPLÉMENTÉ_
- 11 bits d'en-tête : 
  - 3 bits de priorité : de 0 à 7. attention à ne pas set up à 0 par défaut
  - 4 bits pour l’id du destinataire : de 1 à 15
  - 4 bits pour l’id de l’origine : de 1 à 15

cas particulier : 11 bits à 0 : arrêt d’urgence (broadcast) 

raspi : id 1 

herkulex : id 2 

base roulante : id 3 

async : 

[Python Async | Complete Guide to Python Async | Examples](https://www.educba.com/python-async/)

event : 

[Python Event Class | set() Method with Example](https://www.includehelp.com/python/event-set-method-with-example.aspx)

**data herkulex**
- 8 octets (64 bits) de data : 
  - 1 octet commande
  - 1 octet id servo
  - 6 octets de params optionnels, 2 octets par param

**NB** : suivre l’avancement de l’action et renvoyer message de bonne exécution / erreur _IMPLÉMENTÉ_

 ⇒ TODO créer objet herkulex 
  - méthodes avancer/ reculer
  - paramètre nombre de servomoteurs

### main.py 
Futur (?) main du robot. Pour le moment contient juste un appel à la fonction de lecture des aruco codes. 

### tests
Fichiers de tests divers et variés. 
- file.py et utilisation_import.py : fichiers sans intérêt dont je me suis servie pour comprendre le fonctionnement des modules
- simulate_herkulex.py : fichier envoyant un ack pour confirmer la réception d'un message de la raspi comme le ferait un STM quelconque dans le robot
- simulate_robot.py : exemple d'utilisation des fonctions d'envoi et réception de messages en async (comme ce qui devra être fait dans le main du robot) 
