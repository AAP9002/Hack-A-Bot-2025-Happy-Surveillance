
import cv2
from FaceRecogniser import FaceRecogniser

faceRecogniser = FaceRecogniser()
image = cv2.imread("testHappy.png")

# print(image.shape)

print(faceRecogniser.validate(image))