# to start searching the modules from the parent folder
import sys
sys.path.append("..")

import os
import cv2
import unittest

from aruco import ArucoDetector


class TestArucoDetectionRed(unittest.TestCase):

    ar = ArucoDetector()

    RED = "red"

    def test_red(self):
        image_path = os.path.abspath("./datasets/red.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.RED, result[0])

    def test_red_tilted_r(self):
        image_path = os.path.abspath("./datasets/red-tilted-r.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.RED, result[0])

    def test_red_reverse(self):
        image_path = os.path.abspath("./datasets/red-reverse.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.RED, result[0])

    def test_red_tilted_l(self):
        image_path = os.path.abspath("./datasets/red-tilted-l.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.RED, result[0])

if __name__ == '__main__':
    unittest.main(verbosity=3)