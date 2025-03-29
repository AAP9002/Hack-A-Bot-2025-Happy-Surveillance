from modlib.devices import AiCamera
from modlib.apps import Annotator
from modlib.models.zoo import SSDMobileNetV2FPNLite320x320

import cv2

device = AiCamera()
model = SSDMobileNetV2FPNLite320x320()
device.deploy(model)

annotator = Annotator(thickness=1, text_thickness=1, text_scale=0.4)

with device as stream:
    for frame in stream:
        detections = frame.detections[frame.detections.confidence > 0.55]
        labels = [f"{model.labels[class_id]}: {score:0.2f}" for _, score, class_id, _ in detections]
        
        annotator.annotate_boxes(frame, detections, labels=labels)
        
        custom_text = "Custom Text"
        
        # Draw the text on the image (frame.image) using OpenCV's putText method
        cv2.putText(frame.image, 
                    custom_text, 
                    (50, 50),  # Position where the text will be drawn
                    cv2.FONT_HERSHEY_SIMPLEX,  # Font type
                    1,  # Font size
                    (255, 0, 0),  # Text color in BGR (red in this case)
                    2)  # Thickness of the text
        
        frame.display()
