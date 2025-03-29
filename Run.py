from modlib.devices import AiCamera
from modlib.apps import Annotator
from modlib.models.zoo import SSDMobileNetV2FPNLite320x320

import cv2
from sentry.Sentry import Sentry

device = AiCamera()
model = SSDMobileNetV2FPNLite320x320()
device.deploy(model)

annotator = Annotator(thickness=1, text_thickness=1, text_scale=0.4)

sentry = Sentry()

with device as stream:
    for frame in stream:
        detections = frame.detections[frame.detections.confidence > 0.55]
        labels = [f"{model.labels[class_id]}: {score:0.2f}" for _, score, class_id, _ in detections]
        
        annotator.annotate_boxes(frame, detections, labels=labels)
        
        frame_matrix = frame.image

        sentry.process_frame(frame_matrix)
        
        frame.display()
