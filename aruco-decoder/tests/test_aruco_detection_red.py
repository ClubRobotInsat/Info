# to start searching the modules from the parent folder
import sys
sys.path.append("..")

import os
import unittest

from aruco import ArucoDetector


class TestArucoDetectionRed(unittest.TestCase):

    ar = ArucoDetector()

    RED = 47

    def test_red(self):
        result = self.ar.read_image("./datasets/red.jpg")
        self.assertEqual(self.RED, result)

    def test_red_tilted_r(self):
        result = self.ar.read_image("./datasets/red-tilted-r.jpg")
        self.assertEqual(self.RED, result)

    def test_red_reverse(self):
        result = self.ar.read_image("./datasets/red-reverse.jpg")
        self.assertEqual(self.RED, result)

    def test_red_tilted_l(self):
        result = self.ar.read_image("./datasets/red-tilted-l.jpg")
        self.assertEqual(self.RED, result)
