# to start searching the modules from the parent folder
import sys
sys.path.append("..")

import os
import cv2
import unittest

from aruco import ArucoDetector


class TestArucoDetectionGreen(unittest.TestCase):

    ar = ArucoDetector()

    GREEN = "green"

    def test_green(self):
        image_path = os.path.abspath("./datasets/green.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.GREEN, result[0])

    def test_green_tilted_r(self):
        image_path = os.path.abspath("./datasets/green-tilted-r.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.GREEN, result[0])

    def test_green_reverse(self):
        image_path = os.path.abspath("./datasets/green-reverse.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.GREEN, result[0])

    def test_green_tilted_l(self):
        image_path = os.path.abspath("./datasets/green-tilted-l.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.GREEN, result[0])

if __name__ == '__main__':
    unittest.main(verbosity=3)
