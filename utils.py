import os
import cv2 as cv
import numpy as np
import pickle

def create_dataset(dataset_path):
    features = []
    labels = []
    label_map = {}
    current_label = 0

    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)
        if not os.path.isdir(person_path):
            continue

        if person_name not in label_map:
            label_map[person_name] = current_label
            current_label += 1

        label = label_map[person_name]

        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img = cv.resize(img, (200, 200))  # standardize image size
            features.append(img)
            labels.append(label)

    return features, labels

def save_model(model, features, labels, model_path='face_trained.yml', labels_path='labels.pickle'):
    model.write(model_path)

    # Save labels dictionary
    label_dict = {v: k for k, v in enumerate(set(labels))}
    with open(labels_path, 'wb') as f:
        pickle.dump(label_dict, f)
