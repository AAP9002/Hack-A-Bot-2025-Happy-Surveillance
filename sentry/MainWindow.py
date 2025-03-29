import cv2 as cv
from utils.Camera import Camera

class MainWindow():
    def __init__(self):
        self.title = "TOP DOOR SECURITY SYSTEM"
        self.window = None
        self.camera = Camera(0, "Main Camera")
        self.camera.open()
        self.create_window()

    def create_window(self):
        # Create the main window
        self.window = cv.namedWindow(self.title, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.title, 800, 600)

    def tick(self):
        # Update the window with the camera frame
        frame = self.camera.get_frame()
        if frame is None:
            print("Failed to get frame from camera.")
            return
        

        cv.imshow(self.title, frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            self.close()

    def close(self):
        # Close the main window
        pass


main_window = MainWindow()
while True:
    main_window.tick()
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
main_window.camera.release()
cv.destroyAllWindows()