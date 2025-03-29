import cv2 as cv

class Camera:
    def __init__(self, camera_id: int, camera_name: str):
        self.camera_id = camera_id
        self.camera_name = camera_name
        self.capture = None
        self.frame = None

    def open(self):
        # Open the camera
        self.capture = cv.VideoCapture(self.camera_id)
        if not self.capture.isOpened():
            raise Exception(f"Camera {self.camera_name} could not be opened.")
        print(f"Camera {self.camera_name} opened successfully.")
        return self.capture
    
    def get_frame(self):
        # Get a frame from the camera
        if self.capture is None:
            raise Exception(f"Camera {self.camera_name} is not opened.")
        ret, self.frame = self.capture.read()
        if not ret:
            raise Exception(f"Could not read frame from camera {self.camera_name}.")
        return self.frame
    
    def release(self):
        # Release the camera
        if self.capture is not None:
            self.capture.release()
            self.capture = None
            print(f"Camera {self.camera_name} released.")
        else:
            print(f"Camera {self.camera_name} is already released.")

    