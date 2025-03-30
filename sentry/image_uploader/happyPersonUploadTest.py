from ImageUploader import ImageUploader#
import cv2

imageUploader = ImageUploader()

image = cv2.imread("testHappy.png")

imageUploader.add_image_record(image, "happy", "png")