import cv2
from numpy import ndarray

import numpy as np
"""
import the whole module because numpy is needed for creating an array of int32 from
an array of float32
there may be a way not to import the whole module
"""

class ArucoDetector:
    CORRESPONDENCE = {13:"blue", 36:"green", 47:"red", 17:"rock"}

    def __init__(self):
        """A class to detect Aruco code from an image"""
        self.type = cv2.aruco.DICT_4X4_50

    def read_image(self, image):
        """
        Read aruco codes from an image and return values inside and the coordonates
        of the corners of the detected aruco codes

        Args:
            image (ndarray): image to read

        Returns:
            corners_array (ndarray): coordonates of the corners of the aruco codes read
            values (list): Values read from the image
        """
        # load the ArUCo dictionary, grab the ArUCo parameters, and detect the markers
        aruco_dict = cv2.aruco.Dictionary_get(self.type)
        aruco_params = cv2.aruco.DetectorParameters_create()
        corners_array, ids, rejected = cv2.aruco.detectMarkers(image, aruco_dict, parameters=aruco_params)

        # transform float32 array in an int32 array     
        corners_array = np.array(corners_array, np.int32)

        if ids is None:
            values = []
        else:
            # get the corresponding value of the code read
            values = list(self.CORRESPONDENCE.get(id[0]) for id in ids)

        return corners_array, values

    def read_frame(self, frame):
        """
        Read aruco codes from a frame and return values inside and the coordonates
        of the corners of the detected aruco codes

        Args:
            frame (ndarray): Frame to read

        Returns:
            corners_array (ndarray): coordonates of the corners of the aruco codes read
            values (list): Values read from the image
        """
        aruco_dict = cv2.aruco.Dictionary_get(self.type)
        aruco_params = cv2.aruco.DetectorParameters_create()
        corners_array, ids, rejected = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=aruco_params)

        # transform float32 array in an int32 array     
        corners_array = np.array(corners_array, np.int32)

        if ids is None:
            values = []
        else:
            # get the corresponding value of the code read
            values = list(self.CORRESPONDENCE.get(id[0]) for id in ids)

        return corners_array, values
    
    def show_aruco_codes(self, frame, corners_array, values):
        """
        Border aruco codes and show the value above

        Args:
            frame (ndarray): Frame to read
            corners_array (ndarray): coordonates of the corners of the aruco codes
            values (list): Values of the aruco codes

        Returns:
            nothing because the array of the image is modified
        """
        for corners,value in zip(corners_array,values):
            cv2.polylines(frame, corners.astype(int), True, (255,0,255), 3)
            cv2.putText(frame,value,(corners[0][0][0]+10,corners[0][0][1]-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)

