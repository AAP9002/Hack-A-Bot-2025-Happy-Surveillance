import numpy as np
import cv2 as cv
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam, Adamax
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Activation, Dropout, BatchNormalization
from tensorflow.keras import regularizers

from enum import Enum
# from tf.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

"""Enumeration of 7 moods."""
class Mood(Enum):
    ANGRY = 0
    DISGUSTED = 1
    FEARFUL = 2
    HAPPY = 3
    NEUTRAL = 4
    SAD = 5
    SURPRISED = 6

"""Uses a trained model to predict the mood of a person in an image."""
class MoodPredictor:
    imageSize = (224, 224)

    def __init__(self):
        # Setup the tensorflow model
        self.model = tf.keras.models.load_model("sentry/mood_predictor/moodPredictionModel.h5", compile=False)
    
    """
    Loads the saved model weights into the model architecture.

    input: None.
    returns: None.
    """
    def loadWeights(self):
        #Create Model Structure
        img_size = (224, 224)
        channels = 3
        img_shape = (img_size[0], img_size[1], channels)
        class_count = 7 # to define number of classes in dense layer

        # create pre-trained model (you can built on pretrained model such as :  efficientnet, VGG , Resnet )
        # we will use efficientnetb3 from EfficientNet family.
        base_model = tf.keras.applications.efficientnet.EfficientNetB7(include_top= False, weights= "imagenet", input_shape= img_shape, pooling= 'max')
        # base_model.trainable = False
        model = Sequential([
            base_model,
            BatchNormalization(axis= -1, momentum= 0.99, epsilon= 0.001),
            Dense(256, kernel_regularizer= regularizers.l2(0.016), activity_regularizer= regularizers.l1(0.006),
                        bias_regularizer= regularizers.l1(0.006), activation= 'relu'),
            Dropout(rate= 0.45, seed= 123),
            Dense(class_count, activation= 'softmax')
        ])

        model.load_weights("model.h5")
        model.save("sentry/mood_predictor/moodPredictionModel.h5")


    """
    Predicts the mood of the person in the image.
    
    input:
        - image: 3-dim numpy arr.
    
    returns:
        - mood: Mood.
    """
    def predict(self, image):
        # Prepare the image
        preparedImage = self.prepareImage(image)

        # Predict the mood using the model
        predictions = self.model.predict(preparedImage)

        # Choose the class giving the highest prediction 
        predictions = predictions.flatten()
        prediction = np.argmax(predictions)

        return Mood(prediction)
    
    """
    Prepares an image for the model by performing greyscaling and resizing.

    input:
        - image: 3-dim numpy arr.
    
    output:
        - preparedImage: 3-dim numpy arr.
    """
    def prepareImage(self, image):
        # Convert image to greyscale
        greyscaleImage = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

        # Resize the image to imageSize
        greyscaleImage = cv.resize(greyscaleImage, self.imageSize)

        # Duplicate greyscale into 3 channels
        greyscale3Channels = cv.merge([greyscaleImage, greyscaleImage, greyscaleImage])

        # Expand batch dimension
        greyscale3Channels = np.expand_dims(greyscale3Channels, axis=0)  # Shape: (1, 254, 254, 3)

        # Return the prepared image
        return greyscale3Channels