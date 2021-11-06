from aruco import ArucoDetector

ar = ArucoDetector()

img = "./datasets/red.jpg"
print(ar.read_image(img))
