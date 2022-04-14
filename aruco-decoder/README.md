# Aruco Decoder

Decode an aruco code from an image

## Getting Started

### Installation

Clone the repository

```commandline
git clone https://github.com/ClubRobotInsat/Info
```

Install the dependencies
```commandline
pip3 install -r requirements.txt
```

## Project Directories

- [`datasets`](datasets): Stores images for processing and testing
- [`aruco.py`](aruco.py): library
- [`tests`](tests): A bunch of unitary tests

## Usage

### From an image

```python
from aruco import ArucoDetector

ar = ArucoDetector()

# load the image input image
image_path = os.path.abspath("your-image-path")
image = cv2.imread(image_path)

# aruco detection
corners_array, values = ar.read_image(image)
ar.show_aruco_codes(image, corners_array, values)
print(values)
```
Check [image.py](example-image.py)

### From the webcam

Check [camera.py](example-camera.py)

## Unittest

Go to [aruco-decoder](../aruco-decoder) and run the following command

```commandline
python -m unittest discover -s ./tests
```
