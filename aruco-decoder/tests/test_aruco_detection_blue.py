# to start searching the modules from the parent folder
import sys
sys.path.append("..")

import os
import cv2
import unittest

from aruco import ArucoDetector


class TestArucoDetectionBlue(unittest.TestCase):

    ar = ArucoDetector()

    BLUE = "blue"

    def test_blue(self):
        image_path = os.path.abspath("./datasets/blue.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.BLUE, result[0])

    def test_blue_tilted_r(self):
        image_path = os.path.abspath("./datasets/blue-tilted-r.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.BLUE, result[0])

    def test_blue_reverse(self):
        image_path = os.path.abspath("./datasets/blue-reverse.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.BLUE, result[0])

    def test_blue_tilted_l(self):
        image_path = os.path.abspath("./datasets/blue-tilted-l.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.BLUE, result[0])
        


if __name__ == '__main__':
    unittest.main(verbosity=3)
