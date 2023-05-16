"""
#########################################################
            Code Lidar Hokuyo URG-04LX-UG01
#########################################################

module de detection Lidar

v0 : detection adversaire implémentée

Sébastien Vouters, may 2023

"""
import serial
import hokuyo
import serial_port
import numpy as np

class lidar() :
    """
    classe Lidar : Permet le contrôle et l'aqcisition des données du Lidar Hokuyo URG-04LX-UG01
    
    Attributs :
        'LARGEUR_ROBOT': largeur de notre robot,
         'LONGUEUR_ROBOT': longueur de notre robot,
         'SEUIL_MINIMUM_DETECTION': seuil minimum de detection adversaire,
         'LARGEUR_ROBOT_NORME': largeur reglementaire robot,
         'LONGUEUR_ROBOT_NORME': longeur reglementaire robot,
         'ALERTE_DETECTION': seuil maximum de detection adversaire,
         'MIN_ANGLE_DETECTION': filtre angle détection droite,
         'MAX_ANGLE_DETECTION': filtre angle détection gauche,
         'laser_serial': communication serial vers lidar,
         'port': port serie lidar,
         'laser': objet lidar (see hokuyo doc)
         
    Méthodes : 
        get_scan() : Permet de récupérer les données du lidar et de détecter l'adversaire en même temps'
    """
    
    def __init__(self, uart_port) :
        
        # DETECTION ROBOT ADVERSAIRE
            # characteristiques de notre robot
        self.LARGEUR_ROBOT = 290 # en mm pour notre robot
        self.LONGUEUR_ROBOT = 260 # en mm pour notre robot
        self.SEUIL_MINIMUM_DETECTION = (min(self.LARGEUR_ROBOT,self.LONGUEUR_ROBOT)-10)/2 # valeurs en dessous de ce seuil non comptabilisées (-10 pour marge d'erreur)
        
            # characteristiques robot adverse
        self.LARGEUR_ROBOT_NORME = 400 # en mm pour la réglementation de la compétition
        self.LONGUEUR_ROBOT_NORME = 400 # en mm pour la réglementation de la compétition
        self.ALERTE_DETECTION = self.SEUIL_MINIMUM_DETECTION+(max(self.LARGEUR_ROBOT_NORME,self.LONGUEUR_ROBOT_NORME)+10)/2
        
        # FILTRE ANGLE DETECTION LIDAR
        self.MIN_ANGLE_DETECTION = -117
        self.MAX_ANGLE_DETECTION = 120
        
        uart_speed_lidar = 19200
        
        # Initialisation objets et communication laser
        self.laser_serial = serial.Serial(port=uart_port, baudrate=uart_speed_lidar, timeout=0.5)
        self.port = serial_port.SerialPort(self.laser_serial)
        
        # Initialisation du Lidar
        self.laser = hokuyo.Hokuyo(self.port)

        # Initialisation capteur laser / moteur
        print(self.laser.laser_on())
        print(self.laser.set_high_sensitive(False))
        print(self.laser.set_motor_speed(200))
        print('---')
        
    def __del__(self) :
        # Eteignage laser               
        print(self.laser.reset())
        print(self.laser.laser_off())
        del self.laser_serial
        del self.port
        del self.laser
        
    def get_scan(self, coord_cartesienne = False, detect_adversaire = True, affichage = False) :
        """
        Acquisition scan lidar avec detection d'adversaire proche :
            le lidar donne deux listes : distance et angle pour chaque points détectés

        Parameters
        ----------
        coord_cartesienne : bool, optional
            Option de calcul des coordonnées cartésiennes des points détectés. The default is False.
        detect_adversaire : bool, optional
            Option de détection de l'adversaire. The default is True.
        affichage : bool, optional
            Option d'affichage des résultats de la détection de l'adversaire. The default is False.

        Returns
        -------
        distances : list
            Distances de tous les points détectés
        angles : list
            Angles de tous les points détectés
        x : list
            Abscisses de tous les points détectés
        y : list
            Ordonnées de tous les points détectés
        adversaire : bool
            Obstacle détecté

        """
        
        gen = self.laser.get_single_scan() #Lecture du Lidar (renvoie dict{angle:distance})
        
        distances = []
        angles = []
        x = []
        y = []
        adversaire = False
        
        # Calcul des points
        for i in gen.items():
            angle=-i[0] # angle en degrés ; le moins "retourne" l'image pour l'obtenir dans le bon sens
            distance=i[1] # distance en mm
            
            # Tri sur l'angle de détection du lidar
            if (angle > self.MIN_ANGLE_DETECTION) and (angle<self.MAX_ANGLE_DETECTION) :
                distances.append(distance)
                angles.append(angle)
                
                if coord_cartesienne :
                    x.append(distance * np.cos(np.radians(angle)))
                    y.append(distance * np.sin(np.radians(angle)))
                
                if detect_adversaire :
                    if not(adversaire) :
                        adversaire = self.__detect_adversaire__(distance, angle, affichage)
                    else :
                        self.__detect_adversaire__(distance, angle, affichage)
            
        return distances, angles, x, y, adversaire
    
    def __detect_adversaire__(self, distance, angle, affichage) :
        # Recherche les obstacles autour du robot, mais ne prend pas en compte les valeurs trop proches
        adversaire_detecte = (distance>=self.SEUIL_MINIMUM_DETECTION) and (distance<self.ALERTE_DETECTION)
        
        if affichage and adversaire_detecte : 
            print ("Objet détecté" + " à angle : " + str(angle) + "°   , distance :" +str(distance/10) + "cm")
        
        return adversaire_detecte
    
if __name__ == '__main__' :

    uart_port_lidar = '/dev/ttyACM0'
    count = 1000

    i = 0
    objet_lidar = lidar(uart_port_lidar)

    while(i<count) :
        distances, angles, x, y, adversaire = objet_lidar.get_scan(True, True, True)
        plt.xlim(-3000,3000)
        plt.ylim(-3000,3000)
        plt.plot(x,y,'bo', markersize=1)
        plt.pause(0.001)
        plt.clf()
        i += 1
    
    plt.show()
    del objet_lidar