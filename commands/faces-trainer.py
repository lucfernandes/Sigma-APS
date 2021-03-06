import cv2
import os

import numpy as np
from PIL import Image
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "images")


xml_haar_cascade = "cascades/data/haarcascade_frontalface_alt2.xml"

# Carrega o classificador
faceClassifier = cv2.CascadeClassifier(xml_haar_cascade)
recognizer = cv2.face.LBPHFaceRecognizer_create()

#LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}

y_labels = []
x_train = []

# Varre as pastas em busca de imagens registradas
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ", "-").lower()
            # print(label, path)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id+=1
            
            id_ = label_ids[label]
            # print(label_ids)
            #y_labels.append(label) # qualquer numero
            #x_train.append(path) # verifica essa imagem e transforma em um Numpy Array
            pil_image = Image.open(path).convert("L") # grayscale
            size = (550,550)
            final_image = pil_image.resize(size, Image.ANTIALIAS)
            image_array = np.array(final_image, "uint8")
            # print(image_array)
            faces = faceClassifier.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors = 5)

            for (x, y, w, h) in faces:
                roi = image_array[y:y+h, x:x+y]
                x_train.append(roi)
                y_labels.append(id_)
            

# print(y_labels)
# print(x_train)

with open("labels.pickle",'wb') as f:
    pickle.dump(label_ids, f)


recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainner.yml")
