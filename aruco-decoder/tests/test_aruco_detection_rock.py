# to start searching the modules from the parent folder
import sys
sys.path.append("..")

import os
import cv2
import unittest

from aruco import ArucoDetector


class TestArucoDetectionRock(unittest.TestCase):

    ar = ArucoDetector()

    ROCK = "rock"

    def test_rock(self):
        image_path = os.path.abspath("./datasets/rock.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.ROCK, result[0])

    def test_rock_tilted_r(self):
        image_path = os.path.abspath("./datasets/rock-tilted-r.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.ROCK, result[0])

    def test_rock_reverse(self):
        image_path = os.path.abspath("./datasets/rock-reverse.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.ROCK, result[0])

    def test_rock_tilted_l(self):
        image_path = os.path.abspath("./datasets/rock-tilted-l.jpg")
        image = cv2.imread(image_path)
        _, result = self.ar.read_image(image)
        self.assertEqual(self.ROCK, result[0])

if __name__ == '__main__':
    unittest.main(verbosity=3)