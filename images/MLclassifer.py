from keras.applications.mobilenet import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
import numpy as np
import sys

import tensorflow as tf
from keras import backend as K


class MLclassifer:
    def __init__(self):
        num_cores = 4
        num_CPU = 1
        num_GPU = 0

        config = tf.ConfigProto(inter_op_parallelism_threads=num_cores, allow_soft_placement=True,
                                device_count={'CPU': num_CPU, 'GPU': num_GPU})

        session = tf.Session(config=config)
        K.set_session(session)

        r = 224
        a = 0.5
        self.model = MobileNet(include_top=True, weights='imagenet', input_shape=(r, r, 3), alpha=a)

    def classifyPath(self, name):
        img = image.load_img(name, target_size=(224, 224))
        self.classify(self.prepare_image(img))

    def prepare_image(self, img):
        if img.mode != "RGB":
            img = img.convert("RGB")
        img = img.resize((224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        return x

    def classify(self, x):
        x = preprocess_input(x)

        features = self.model.predict(x)

        tags = []

        for item in decode_predictions(features, 10)[0]:
            print((item[1] + ":                 ")[0:20] + str(item[2] * 100)[0:5] + "%")
            if (item[2] > 0.005):
                tags.append(item[1] + ":  " + str(item[2] * 100).split(".")[0] + "%")
        return tags
