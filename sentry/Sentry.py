from numpy import add
import cv2
from gpiozero import Servo
from time import sleep
from .mood_predictor.MoodPredictor import Mood, MoodPredictor

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
        return mood
    
    def fire_shin_attack(self):
        self.servo.min()
        sleep(1)
        self.servo.max()
        sleep(1)


   