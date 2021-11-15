# to start searching the modules from the parent folder
import sys
sys.path.append("..")

import os
import unittest

from aruco import ArucoDetector


class TestArucoDetectionRock(unittest.TestCase):

    ar = ArucoDetector()

    ROCK = 17

    def test_rock(self):
        result = self.ar.read_image("./datasets/rock.jpg")
        self.assertEqual(self.ROCK, result)

    def test_rock_tilted_r(self):
        result = self.ar.read_image("./datasets/rock-tilted-r.jpg")
        self.assertEqual(self.ROCK, result)

    def test_rock_reverse(self):
        result = self.ar.read_image("./datasets/rock-reverse.jpg")
        self.assertEqual(self.ROCK, result)

    def test_rock_tilted_l(self):
        result = self.ar.read_image("./datasets/rock-tilted-l.jpg")
        self.assertEqual(self.ROCK, result)
