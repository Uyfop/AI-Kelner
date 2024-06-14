import cv2
import numpy as np
import tensorflow as tf

def prepare_image(file):
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (64, 64))
    img = img.astype("float") / 255.0
    img = np.reshape(img, (1, 64, 64, 1))
    return img

def main():
    file_name = "plate.jpg"
    model = tf.keras.models.load_model('../../plate_classifier_model.keras')

    img = prepare_image(file_name)
    prediction = model.predict(img)
    if prediction > 0.5:
        print("full")
    else:
        print("empty")

main()
