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
    "delCorupt",
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


# plt.show()
# plt.figure(figsize=(10,10))
# for i in range(10):
#     plt.subplot(5,5,i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.grid(False)
#     for batch_x, batch_y in train_data[0]:
#         x = batch_x[i]
#         x = (x / 255)
#         print(x.shape)
#         plt.imshow(x)
# plt.show()

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10))

model.compile(optimizer='adam',
              loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

train_images = [0] * 5
train_labels = [0] * 5

for i in range(5):
    for batch_x, batch_y in train_data[0]:
        train_images[i] = batch_x[i]/255
        train_labels[i] = batch_y[i]/255

history = model.fit(train_data[0], epochs=10,
                  validation_data=train_data[1])
model.summary()