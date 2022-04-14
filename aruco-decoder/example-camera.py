import cv2

from aruco import ArucoDetector

cam = cv2.VideoCapture(0)
ar = ArucoDetector()

while True:
    _, frame = cam.read()

    # aruco detection
    corners_array, values = ar.read_image(frame)
    ar.show_aruco_codes(frame, corners_array, values)

    cv2.imshow('Input', frame)

    if len(values) > 0:
        print(values)

    c = cv2.waitKey(100)

    if c == 27:
        break

cam.release()
cv2.destroyAllWindows()
