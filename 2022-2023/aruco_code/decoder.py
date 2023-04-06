import cv2
import imutils
from math import sqrt
# si le code ne détecte pas, vérifier bien le type d'aruco code et s'il est entourée d'un carré blanc

def read():
    cap = cv2.VideoCapture(0)  # id 0 camera standard système
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)  # style TODO utiliser celui de la compete
    aruco_params = cv2.aruco.DetectorParameters_create()
    taille_frame = 1000 #Taille de la frame
    if not cap.isOpened():
        raise "error opening video input"

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            frame = imutils.resize(frame, width=taille_frame)  # resize chaque frame en 1000x1000
            (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, aruco_dict,
                                                            parameters=aruco_params)  # corners position dans la frame
            # des coins du code
            # id de touts les codes détectés(peut-être liste de int)
            #
            # if len(rejected)>0:
            #     print(rejected)
            if len(corners) > 0:  # si code détecté,
                ###print("code détecté")
                ids = ids.flatten()  # affiche dans le frame video la position des codes et leur ID
                for (markerCorner, markerID) in zip(corners, ids):
                    corners = markerCorner.reshape((4, 2))
                    (topLeft, topRight, bottomRight, bottomLeft) = corners

                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))
                    ##Calcul de la proportion du code dans l'image pour évaluer distance##
                    proportion_top = sqrt((topRight[1]-topLeft[1])**2+(topRight[0]-topLeft[0])**2)/taille_frame ##Calcul de la proportion ligne haute
                    proportion_bottom = sqrt((bottomRight[1]-bottomLeft[1])**2+(bottomRight[0]-bottomLeft[0])**2)/taille_frame ##Calcul proportion basse
                    prop_moy = (proportion_bottom+proportion_top)/2 ## Proportion moyenne
                    distance = -606.1695*prop_moy + 93.0743 #TODO recalculer la fonction de régression linéaire avec vrai conditions
                    ##Pour mesurer distance en fonction de prop_moy et calculer la fonction
                    cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
                    cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
                    cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
                    cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                    cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)

                    cv2.putText(frame, str(markerID),
                                (topLeft[0], topLeft[1] - 15),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 2)

                cv2.imshow("Frame", frame)  # affiche frame dans l'écran TODO à enlever quand debug sera finit

            cv2.imshow('Frame', frame)
            if cv2.waitKey(25) & 0XFF == ord('q'):  # fermeture fenêtre video
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
