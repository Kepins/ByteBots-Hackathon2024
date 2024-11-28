import os
from cProfile import label

import numpy as np
import keras
import tensorflow as tf
from keras import layers, models, datasets
from tensorflow import data as tf_data
import matplotlib.pyplot as plt

image_size= (200, 200)
batch_size = 32

train_data = keras.utils.image_dataset_from_directory(
    "train",
    labels="inferred",
    validation_split=0.1,
    subset="both",
    seed=1337,
    image_size=image_size,
    batch_size=32,
    verbose=1
)
class_names = train_data[0].class_names

print(type(train_data[1]))

print(len(train_data[0]))


plt.show()
plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    for batch_x, batch_y in train_data[0]:
        x = np.asarray(batch_x[1])
        x = (x / 255)
        print(x.shape)
        plt.imshow(x)

plt.show()