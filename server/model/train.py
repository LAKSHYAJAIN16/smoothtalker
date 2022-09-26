import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import Embedding, Dense, LSTM, SimpleRNN
from keras.callbacks import ModelCheckpoint

# Define Data Locations
x_data = []
y_data = []

# Load Data
with open('data/pickle/xTrain.pkl', 'rb') as f:
    x_data = np.array(pickle.load(f))
with open('data/pickle/yTrain.pkl', 'rb') as f:
    y_data = np.array(pickle.load(f))

# Get Train & Test
X_train, X_test, y_train, y_test = train_test_split(x_data, y_data,
                                                    test_size=0.25,
                                                    shuffle=True)

# Define N
NX = len(x_data[0])
NY = len(y_data[0])
print(x_data)

# Checkpoint
checkpoint1 = ModelCheckpoint("best_model.hdf5", monitor='val_accuracy', verbose=1,
                              save_best_only=True, mode='auto', period=1, save_weights_only=False)

# Create Model
model = Sequential()
model.add(Embedding(5000, 40))
model.add(Dense(128, activation="relu"))
model.add(LSTM(64, dropout=0.5))
model.add(Dense(32, activation="relu"))
model.add(Dense(16, activation="relu"))
model.add(Dense(8, activation="relu"))
model.add(Dense(4, activation="relu"))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy', metrics=['accuracy'])

hist = model.fit(X_train, y_train,
                 epochs=300,
                 verbose=1,
                 validation_data=(X_test, y_test),
                 callbacks=[checkpoint1]
                 )
