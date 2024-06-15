import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import tensorflow as tf
from PIL import Image


class PlateClassifier:
    def __init__(self):
        self.model = self._load_model()

    def _load_model(self):
        return tf.keras.models.load_model('./plate_classifier_model.keras')
    
    def _prepare_image(self, file_path: str):
        img = Image.open(file_path).convert("L")
        img = img.resize((64, 64))
        img = np.array(img).astype("float") / 255.0
        img = np.reshape(img, (1, 64, 64, 1))
        return img

    def predict(self, file_path: str) -> float:
        img = self._prepare_image(file_path)
        prediction = self.model.predict(img, verbose=0)
        return prediction
