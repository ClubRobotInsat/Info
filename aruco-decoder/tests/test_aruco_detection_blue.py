# to start searching the modules from the parent folder
import sys
sys.path.append("..")

import os
import unittest

from aruco import ArucoDetector


class TestArucoDetectionBlue(unittest.TestCase):

    ar = ArucoDetector()

    BLUE = 13

    def test_blue(self):
        result = self.ar.read_image("./datasets/blue.jpg")
        self.assertEqual(self.BLUE, result)

    def test_blue_tilted_r(self):
        result = self.ar.read_image("./datasets/blue-tilted-r.jpg")
        self.assertEqual(self.BLUE, result)

    def test_blue_reverse(self):
        result = self.ar.read_image("./datasets/blue-reverse.jpg")
        self.assertEqual(self.BLUE, result)

    def test_blue_tilted_l(self):
        result = self.ar.read_image("./datasets/blue-tilted-l.jpg")
        self.assertEqual(self.BLUE, result)


if __name__ == '__main__':
    unittest.main(verbosity=3)
