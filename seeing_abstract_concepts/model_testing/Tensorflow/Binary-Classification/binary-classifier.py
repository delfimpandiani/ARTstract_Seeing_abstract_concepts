# This model uses the fresh / non fresh data from ARTEMIS. It is based onthis tutorial [https://www.youtube.com/watch?v=jztwpsIzEGc]  by Nicholas Renotte
# It executes a binary classification model

import os
import cv2
import imghdr
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.metrics import Precision, Recall, BinaryAccuracy
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout


# ------------------LOAD DATA------------------
data_dir = 'freshness_data' 
data = tf.keras.utils.image_dataset_from_directory(data_dir) #Found 1258 files belonging to 2 classes.

data_iterator = data.as_numpy_iterator()
batch = data_iterator.next()

# Check out some images from the first batch
fig, ax = plt.subplots(ncols=4, figsize=(20,20))
for idx, img in enumerate(batch[0][:4]):
    ax[idx].imshow(img.astype(int))
    ax[idx].title.set_text(batch[1][idx])


# ------------------SCALE DATA------------------

data = data.map(lambda x,y: (x/255, y))
data.as_numpy_iterator().next()

# ------------------SCALE DATA------------------

train_size = int(len(data)*.7)
val_size = int(len(data)*.2)
test_size = int(len(data)*.1)

train = data.take(train_size)
val = data.skip(train_size).take(val_size)
test = data.skip(train_size+val_size).take(test_size)

# ------------------BUILD THE MODEL------------------

model = Sequential([
    Conv2D(16, (3,3), 1, activation='relu', input_shape=(256,256,3)),
    MaxPooling2D(),
    Conv2D(32, (3,3), 1, activation='relu'),
    MaxPooling2D(),
    Conv2D(16, (3,3), 1, activation='relu'),
    MaxPooling2D(),
    Flatten(),
    Dense(256, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile('adam', loss=tf.losses.BinaryCrossentropy(), metrics=['accuracy'])
model.summary()

# ------------------TRAIN THE MODEL------------------

logdir='logs'
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
hist = model.fit(train, epochs=20, validation_data=val, callbacks=[tensorboard_callback])


# ------------------PLOT PERFORMANCE------------------

# Plotting loss
fig = plt.figure()
plt.plot(hist.history['loss'], color='teal', label='loss')
plt.plot(hist.history['val_loss'], color='orange', label='val_loss')
fig.suptitle('Loss', fontsize=20)
plt.legend(loc="upper left")
plt.show()

# Plotting accuracy
fig = plt.figure()
plt.plot(hist.history['accuracy'], color='teal', label='accuracy')
plt.plot(hist.history['val_accuracy'], color='orange', label='val_accuracy')
fig.suptitle('Accuracy', fontsize=20)
plt.legend(loc="upper left")
plt.show()


# ------------------EVALUATE------------------

pre = Precision()
re = Recall()
acc = BinaryAccuracy()

for batch in test.as_numpy_iterator(): 
    X, y = batch # the image and the true value
    yhat = model.predict(X) # the prediction value
    pre.update_state(y, yhat)
    re.update_state(y, yhat)
    acc.update_state(y, yhat)

    print(f'Precision:{pre.result().numpy()}, Recall: {re.result().numpy()}, Accuracy:{acc.result().numpy()}')


# ------------------TEST NEW IMAGES------------------

img = cv2.imread('fresh.jpg')
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()

resize = tf.image.resize(img, (256,256))
plt.imshow(resize.numpy().astype(int))
plt.show()

yhat = model.predict(np.expand_dims(resize/255, 0))
# we do this bc the modele expects a batch of images, not just one

if yhat > 0.5: 
    print(f'Predicted class is the first one')
else:
    print(f'Predicted class is the second one')

# ------------------SAVE THE MODEL------------------

model.save(os.path.join('models','imageclassifier.h5'))
new_model = load_model('models/imageclassifier.h5')

# Use the loaded model to check that it still gives the same prediction 
yhatnew = new_model.predict(np.expand_dims(resize/255, 0))
if yhatnew > 0.5:
    print(f'Predicted class is the first one')
else:
    print(f'Predicted class is the second one')

