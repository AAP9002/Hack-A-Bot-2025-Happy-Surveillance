from MoodPredictor import Mood, MoodPredictor
import cv2 as cv

# Create the mood predictor class
moodPredictor = MoodPredictor()

# # test on test image
testImage = cv.imread("sentry/mood_predictor/testHappy.png")

result = moodPredictor.predict(testImage)
print(result)