import tensorflow as tf
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
from pymongo import MongoClient
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime, timezone
import cv2
import os
import os
import base64

class FaceRecogniser():
    VALIDATION_THRESHOLD = 0.2

    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get MongoDB connection URI from .env
        self.mongo_uri = os.getenv("MONGODB_URI")

        # Load the MTCNN for face detection
        self.mtcnn = MTCNN(keep_all=True)
        self.model = InceptionResnetV1(pretrained='vggface2').eval()
    
    def convert_numpy_image_to_base64(self, image_np, image_type="png"):
        """Convert a NumPy image array to a base64-encoded string."""
        _, buffer = cv2.imencode(f".{image_type}", image_np)
        return base64.b64encode(buffer).decode('utf-8')
    
    def get_face_embedding(self, image):
        # Convert to Image object
        face_image_pil = Image.fromarray(image)

        # Resize the image to 160x160 pixels (required input size for FaceNet)
        face_image_resized = face_image_pil.resize((160, 160))
        
        # Detect faces using MTCNN
        faces = self.mtcnn(face_image_resized)
        
        if faces is None:
            return None  # No faces detected
        
        first_face = faces[0].unsqueeze(0)
        
        # Get the embeddings for all detected faces
        embeddings = self.model(first_face)
        
        return embeddings.detach().cpu().numpy().flatten()  # convert to np then flatten to 1D
    
    def compare_faces(self, embedding1, embedding2):
        # Compute the Euclidean distance between the two embeddings
        dist = np.linalg.norm(embedding1 - embedding2)
        return dist
        
    
    def add_new_face(self, image):
        # Get the embedding for the face
        embedding_list = self.get_face_embedding(image).tolist()

        # Prepare the MongoDB document
        face_data = {
            'embedding': embedding_list,  # Store the embedding as a list
            'face': self.convert_numpy_image_to_base64(image, "png"),
            'timestamp': datetime.now(timezone.utc)
        }

        # Connect to MongoDB (assuming MongoDB is running locally)
        client = MongoClient(self.mongo_uri)
        db = client['face_recognition']  # Database name
        collection = db['face_embeddings']  # Collection name

        # Insert the document into the MongoDB collection
        collection.insert_one(face_data)

        print("New face added.")
    
    def validate(self, image):
        # Get the embedding for the image
        embedding = self.get_face_embedding(image)

        # Connect to MongoDB
        client = MongoClient(self.mongo_uri)
        db = client['face_recognition']
        collection = db['face_embeddings']

        # Retrieve all embeddings from MongoDB
        cursor = collection.find()

        # List to store similarity results
        isValidated = False

        # Compare the new embedding with each stored embedding
        for document in cursor:
            stored_embedding = np.array(document['embedding'])  # Retrieve the stored embedding
            loss = self.compare_faces(embedding, stored_embedding)  # Compare with stored embeddings

            if loss < self.VALIDATION_THRESHOLD:
                isValidated = True
                break
        
        return isValidated
