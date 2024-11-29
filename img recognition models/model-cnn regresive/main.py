import os
from cProfile import label
import numpy as np
import keras
import tensorflow as tf
from keras import layers, models, datasets, callbacks
from keras.src.layers import average
from tensorflow import data as tf_data
import matplotlib.pyplot as plt

image_size= (200, 200)

train_data = keras.utils.image_dataset_from_directory(
    "img/train",
    labels="inferred",
    seed=1337,
    image_size=image_size,
    batch_size=128,
    verbose=1
)

val_data = keras.utils.image_dataset_from_directory(
    "img/val",
    labels="inferred",
    seed=1337,
    image_size=image_size,
    batch_size=64,
    verbose=1
)

class_names = train_data.class_names

#model load
model = keras.models.load_model("model.keras")

#model
# model = models.Sequential()
# model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 3)))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
#
# model.add(layers.Flatten())
# model.add(layers.Dense(128, activation='relu'))
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dense(1))
#
# model.compile(optimizer='adam',
#               loss=keras.losses.MeanSquaredError(),
#               metrics=[keras.metrics.MeanAbsoluteError()])

checkpoint = callbacks.ModelCheckpoint(
        filepath=f'model.keras',
        verbose=1,
        monitor='val_mean_absolute_error',
        save_best_only=True,
        mode='min'
    )

history = model.fit(train_data, epochs=200,
                    validation_data=val_data,
                    callbacks=[checkpoint])


# test_data = keras.utils.image_dataset_from_directory(
#     "img/test",
#     labels="inferred",
#     seed=1337,
#     image_size=image_size,
#     batch_size=64,
#     verbose=1
# )

#prediction = model.predict(test_data)

# meanError = []
# for i in range(len(test_data)):
#     meanError.append(prediction[i] - test_data[i])


# print("max: ", max(prediction))
# print("min: ", min(prediction))

model.summary()