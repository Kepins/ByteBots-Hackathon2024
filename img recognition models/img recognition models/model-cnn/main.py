import keras
import tensorflow as tf
from keras import layers, models, callbacks

tf.config.list_physical_devices('GPU')

image_size= (200, 200)
batch_size = 32

train_data = keras.utils.image_dataset_from_directory(
    "img/train",
    labels="inferred",
    seed=1337,
    image_size=image_size,
    batch_size=64,
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

#model
#model = keras.models.load_model("model.keras")

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(5))

model.compile(optimizer='adam',
              loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

theroids_type = 5

train_images = [0] * theroids_type
train_labels = [0] * theroids_type

for i in range(theroids_type):
    for batch_x, batch_y in train_data:
        train_images[i] = batch_x[i]/255
        train_labels[i] = batch_y[i]/255

val_images = [0] * theroids_type
val_labels = [0] * theroids_type

for i in range(theroids_type):
    for batch_x, batch_y in val_data:
        val_images[i] = batch_x[i]/255
        val_labels[i] = batch_y[i]/255

checkpoint = callbacks.ModelCheckpoint(
        filepath=f'model.keras',
        verbose=1,
        monitor='val_accuracy',
        save_best_only=True,
        mode='max'
    )

history = model.fit(train_data, epochs=200,
                    validation_data=val_data,
                    callbacks=[checkpoint])

model.summary()