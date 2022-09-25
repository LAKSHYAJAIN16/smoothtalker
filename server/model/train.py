import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import Embedding, Dense, LSTM, SimpleRNN

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

# Create Model
model = Sequential()
model.add(Embedding(5000, 40))
model.add(Dense(100, activation="relu"))
model.add(SimpleRNN(35, return_sequences=True))
model.add(SimpleRNN(35))
model.add(Dense(4, activation="relu"))
model.compile(optimizer='adam',
              loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train,
          batch_size=200,
          epochs=300,
          verbose=1,
          validation_data=(X_test, y_test))
