import cv2
import os

from aruco import ArucoDetector

ar = ArucoDetector()

# load the image input image from disk
image_path = os.path.abspath("datasets/aruco-cdf.jpg")
image = cv2.imread(image_path)

# aruco detection
corners_array, values = ar.read_image(image)
ar.show_aruco_codes(image, corners_array, values)
print(values)

cv2.imshow('Image', image)
cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image