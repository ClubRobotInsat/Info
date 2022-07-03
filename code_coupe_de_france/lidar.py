"""
#########################################################
            Code Lidar Hokuyo URG-04LX-UG01
#########################################################

Code Effectuant la reconnaissance d'obstacles proches et l'affichage des points

Commentaire :
En output on obtient l'angle en degrés avec pour référence : 180° le coté "aveugle" du lidar (avec la languette)

Sébastien Vouters, may 2022

"""
import serial
import hokuyo
import serial_port
from api_envoi import envoyer
import utiles

LARGEUR_ROBOT = 400  # en mm pour notre robot
LONGUEUR_ROBOT = 400  # en mm pour notre robot
SEUIL_MINIMUM_DETECTION = (min(LARGEUR_ROBOT,
                               LONGUEUR_ROBOT) - 10) / 2  # valeurs en dessous de ce seuil non comptabilisées (-10
# pour marge d'erreur)
LARGEUR_ROBOT_NORME = 400  # en mm pour la réglementation de la compétition
LONGUEUR_ROBOT_NORME = 400  # en mm pour la réglementation de la compétition
ALERTE_DETECTION = SEUIL_MINIMUM_DETECTION + (min(LARGEUR_ROBOT_NORME, LONGUEUR_ROBOT_NORME) + 10) / 2

# uart_port = '/dev/ttyACM0' linux
uart_port = 'COM22'  # Windows : à modifier à chaque rebranchement
uart_speed = 19200


def initialisation():
    # Initialisation objets et communication laser
    laser_serial = serial.Serial(port=uart_port, baudrate=uart_speed, timeout=0.5)
    port = serial_port.SerialPort(laser_serial)

    laser = hokuyo.Hokuyo(port)

    # Initialisation laser
    print(laser.laser_on())
    print('---')
    print(laser.set_high_sensitive(False))
    print('---')
    print(laser.set_motor_speed(200))
    print('---')
    return laser


# obstacle=False
# while (not(obstacle)) :

def detection(laser, buffer_acks, ack_received_cond, buffer_lock):
    id_motor = 3  # TODO : vraie valeur
    data_stop_moteur = ['00', '00', '00', '00', '00', '00']  # TODO : vraie valeur
    message_stop_moteur = utiles.Message(id_motor, utiles.id_raspi, data_stop_moteur)
    while True:
        gen = laser.get_single_scan()  # Lecture du Lidar (renvoie dict{angle:distance})

        # Calcul des points
        for i in gen.items():
            angle = -i[0]  # en degrés ; le moins "retourne" l'image pour l'obtenir dans le bon sens
            distance = i[1]  # en mm
            if distance >= SEUIL_MINIMUM_DETECTION:  # Ne prend pas en compte les valeurs trop proches
                if distance < ALERTE_DETECTION:  # Detection des points proches au robot
                    # obstacle=True
                    envoyer(message_stop_moteur, buffer_acks, ack_received_cond, buffer_lock)
                    print("Objet détecté" + " à angle : " + str(angle) + "°   , distance :" + str(distance / 10) + "cm")


def eteindre(laser):
    # Eteignage laser
    print(laser.reset())
    print('---')
    print(laser.laser_off())
