# -*- coding: utf-8 -*-
"""FER HoGaya Model 1_Face.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GIwh0eW57dqeFAaR7kt5TtbmkGXFataE
"""

from tensorflow import keras
# from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

# from google.colab import drive
# drive.mount('/content/drive')

model = keras.models.load_model(r"C:\Users\AMAN YADAV\Downloads\fer_best.h5")

model.summary()

emotions = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy',
            4: 'neutral', 5: 'sad', 6: 'surprise'}





face_cascade = cv2.CascadeClassifier()

face_cascade.load(cv2.data.haarcascades +
                 './haarcascade_frontalface_alt2.xml')

def show_img(img):
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def load_img(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img



# # from google.colab import files

# uploaded_file = 

# # new_file = next(iter(uploaded_file))

# image = cv2.imread(new_file)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
def emotion_recog(path_img):
    print(f"Attempting to load image from: {path_img}")

    # Check if file exists
    if not os.path.isfile(path_img):
        raise FileNotFoundError(f"The file {path_img} does not exist.")

    # Read the image
    image = cv2.imread(path_img)

    # Check if image was successfully loaded
    if image is None:
        raise ValueError(f"Unable to load image: {path_img}")


    #show_img(image)

    face_pos = face_cascade.detectMultiScale(image, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in face_pos:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    #show_img(image)

    cropped_img = image[y:y+h, x:x+h]
    #show_img(cropped_img)



    def face_processing(face):
        face = cv2.cvtColor(face, cv2.COLOR_RGB2GRAY)
        face = cv2.resize(face, (48, 48))
        face = np.expand_dims(face, axis=0)
        face = np.expand_dims(face, -1)
        face = face / 255.0
        return face

    face = face_processing(cropped_img)

    def get_preds(face):
        preds = model.predict(face)
        emotion = emotions[np.argmax(preds)]
        prob = round(np.max(preds) * 100, 2)
        return emotion, prob

    label, prob = get_preds(face)

    image = cv2.putText(image, label, (x-10, y-10),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), thickness=2)

    #show_img(image)
    print(f'Emotion: {label}, with prob: {prob}')
    return label

