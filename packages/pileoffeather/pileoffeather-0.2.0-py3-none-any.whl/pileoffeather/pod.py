import cv2
import numpy as np
import os

def saveImage(vector, image_path, image_size, color):
    if color == "grayscale":
        vector = (vector * 255.0).reshape(image_size).astype(np.uint8)
        vector = cv2.cvtColor(vector, cv2.COLOR_GRAY2BGR)
    else:
        vector = (vector * 255.0).reshape(image_size + (3,)).astype(np.uint8)
    cv2.imwrite(image_path, vector)

def loadImage(image_path, desired_size, color):
    image = cv2.imread(image_path)
    image = cv2.resize(image, desired_size)
    if color == "grayscale":
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    vectorized_image = image.flatten() / 255.0
    return vectorized_image

def load(**options):
    data_type = options.get("data_type")
    match data_type:
        case "image":
            folder = options.get("folder")
            resize = options.get("resize")
            file_names = os.listdir(folder)
            all_images_vector = []
            for file_name in file_names:
                image_vector = loadImage(folder + "/" + file_name, resize, options.get("color"))
                all_images_vector.append(image_vector)
            return np.vstack(all_images_vector)
