class Sentry():
    def process_frame(self, frame):
        # This method should be overridden in subclasses
        raise NotImplementedError("Subclasses should implement this method.")
    
    def classify_mood(self, frame):
        # This method should be overridden in subclasses
        raise NotImplementedError("Subclasses should implement this method.")
    
    def find_face(self, frame):
        # This method should be overridden in subclasses
        raise NotImplementedError("Subclasses should implement this method.")
    
    def add_text(self, frame, text):
        # This method should be overridden in subclasses
        raise NotImplementedError("Subclasses should implement this method.")
    
    def notify_system(self, message):
        # This method should be overridden in subclasses
        raise NotImplementedError("Subclasses should implement this method.")