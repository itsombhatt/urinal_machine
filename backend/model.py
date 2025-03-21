import pandas as pd

from keras.models import Sequential, Model
from keras.layers import Dense, Input
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures

from sklearn.model_selection import train_test_split
import warnings 
warnings.filterwarnings('ignore')

data = pd.read_csv("backend/data.csv")
X = data.drop("position", axis=1).values
y = data.position.values

poly = PolynomialFeatures(degree=2, include_bias=True)
transformed_data = poly.fit_transform(X)
print(transformed_data.shape)

X_train, X_test, y_train, y_test = train_test_split(transformed_data, y, test_size=0.16, random_state = 42)

model = Sequential()
model.add(Dense(20, input_shape=(transformed_data.shape[1],), activation = 'tanh'))
model.add(Dense(12, activation='tanh'))
model.add(Dense(5, activation='softmax'))

model.compile(optimizer='SGD', loss='sparse_categorical_crossentropy', metrics=['sparse_categorical_accuracy'])

model.fit(X_train, y_train, epochs=250, batch_size=256, verbose=0)

model.evaluate(X_test, y_test)