from numpy import add
import cv2
from gpiozero import Servo
from time import sleep
from .mood_predictor.MoodPredictor import Mood, MoodPredictor
from .image_uploader.ImageUploader import ImageUploader
from .face_recognition.FaceRecogniser import FaceRecogniser

class Sentry():
    def __init__(self):
        self.moodPredictor = MoodPredictor()
        self.moodEnum = Mood
        # Define pulse widths based on your servo's specifications
        min_pulse = 1 / 1000  # 1ms pulse width
        max_pulse = 2 / 1000  # 2ms pulse width

        # Initialize the servo with custom pulse widths
        self.servo = Servo(18, min_pulse_width=min_pulse, max_pulse_width=max_pulse)
        self.servo.min()

        self.face_recogniser = FaceRecogniser()


    def add_system_name(self, frame, name):
        """add the device name in the top left corner with an active status

        Args:
            name (str): the text to add
        """
        cv2.putText(frame,
                    name,  # Text to display
                    (10, 30),  # Position where the text will be drawn
                    cv2.FONT_HERSHEY_SIMPLEX,  # Font type
                    1,  # Font size
                    (255, 0, 0),  # Text color in BGR (red in this case)
                    2)
        


    def process_frame(self, frame):
        # This method should be overridden in subclasses
        self.add_system_name(frame, "Sentry System: Active")
    
    def classify_mood(self, face_image):
        # This method should be overridden in subclasses
        # Assuming the frame is a numpy array (image)
        mood = self.moodPredictor.predict(face_image)
        self.add_image_record(face_image, mood.name)
        return mood
    
    def fire_shin_attack(self):
        self.servo.min()
        sleep(1)
        self.servo.max()
        sleep(1)

    def add_image_record(self, image, emotion):
        """Add an image record to the database."""
        # Assuming the image is a numpy array (image)
        image_uploader = ImageUploader()
        image_uploader.add_image_record(image, emotion)
        print("Image record added to the database.")

    def check_face_recognition(self, face_image):
        # This method should be overridden in subclasses
        status = self.face_recogniser.validate(face_image)
        print(f"Face recognition status: {status}")
        return status

   