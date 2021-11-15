# to start searching the modules from the parent folder
import sys
sys.path.append("..")

import os
import unittest

from aruco import ArucoDetector


class TestArucoDetectionGreen(unittest.TestCase):

    ar = ArucoDetector()

    GREEN = 36

    def test_green(self):
        result = self.ar.read_image("./datasets/green.jpg")
        self.assertEqual(self.GREEN, result)

    def test_green_tilted_r(self):
        result = self.ar.read_image("./datasets/green-tilted-r.jpg")
        self.assertEqual(self.GREEN, result)

    def test_green_reverse(self):
        result = self.ar.read_image("./datasets/green-reverse.jpg")
        self.assertEqual(self.GREEN, result)

    def test_green_tilted_l(self):
        result = self.ar.read_image("./datasets/green-tilted-l.jpg")
        self.assertEqual(self.GREEN, result)
