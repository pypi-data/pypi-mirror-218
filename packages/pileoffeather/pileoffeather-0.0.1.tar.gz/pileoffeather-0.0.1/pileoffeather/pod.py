import cv2
import numpy as np
import os

def loadImage(image_path, desired_size):
    color_image = cv2.imread(image_path)
    resized_image = cv2.resize(color_image, desired_size)
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    vectorized_image = gray_image.flatten() / 255.0
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
                image_vector = loadImage(folder + "/" + file_name, resize)
                all_images_vector.append(image_vector)
            return np.vstack(all_images_vector)
