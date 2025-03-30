from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from datetime import datetime, timezone

import os
import base64
import cv2

class ImageUploader:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get MongoDB connection URI from .env
        self.mongo_uri = os.getenv("MONGODB_URI")
        print(self.mongo_uri)
        
        # Connect to MongoDB Atlas
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client['people_emotions']
        self.collection = self.db['emotion_records']

    def convert_numpy_image_to_base64(self, image_np, image_type="png"):
        """Convert a NumPy image array to a base64-encoded string."""
        _, buffer = cv2.imencode(f".{image_type}", image_np)
        return base64.b64encode(buffer).decode('utf-8')

    def add_image_record(self, image, emotion, image_type="png"):
        """Insert a new image record into the database."""
        record = {
            "image": self.convert_numpy_image_to_base64(image, image_type),
            "emotion": emotion,
            "image_type": image_type,
            "date_added": datetime.now(timezone.utc)  # Store timestamp in UTC
        }
        
        # Insert record and return the inserted document ID
        inserted_doc = self.collection.insert_one(record)

        print("Successfully added new image. Id: " + str(inserted_doc.inserted_id))