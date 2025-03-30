from gpiozero import Servo
from time import sleep

# Define pulse widths based on your servo's specifications
min_pulse = 1 / 1000  # 1ms pulse width
max_pulse = 2 / 1000  # 2ms pulse width

# Initialize the servo with custom pulse widths
servo = Servo(18, min_pulse_width=min_pulse, max_pulse_width=max_pulse)

try:
    while True:
        servo.min()  # Move to minimum position
        sleep(1)
        servo.mid()  # Move to middle position
        sleep(1)
        servo.max()  # Move to maximum position
        sleep(1)
except KeyboardInterrupt:
    pass

