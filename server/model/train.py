import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import Dense, Dropout

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
                                                    random_state=104,
                                                    test_size=0.25,
                                                    shuffle=True)

# Define N
NX = len(x_data[0])
NY = len(y_data[0])
print(x_data)

# Create Model
model = Sequential()
model.add(Dense(NX, activation="sigmoid", name="layer1"))
model.add(Dropout(0.5))
model.add(Dense(100, activation="relu", name="layer2"))
model.add(Dropout(0.5))
model.add(Dense(100, activation="sigmoid", name="layer3"))
model.add(Dropout(0.5))
model.add(Dense(NY, activation="sigmoid", name="layer4"))
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train,
          batch_size=500,
          epochs=100,
          verbose=1,
          validation_data=(X_test, y_test))
