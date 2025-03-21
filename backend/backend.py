from flask import Flask, request, jsonify
import logging
import csv

from flask_cors import CORS

import pandas as pd
import numpy as np

from keras.models import Sequential, Model
from keras.layers import Dense, Input
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures

from sklearn.model_selection import train_test_split
import warnings 
warnings.filterwarnings('ignore')
app = Flask(__name__)
CORS(app, origins=["*"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data = []

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

def writeToCSV(entry):
    print(entry)
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(entry) 

@app.route('/', methods=['GET'])
def main_page():
    return jsonify({
        'Goated?': 'Alex',
        'Mid?': 'Om',
    })

@app.route('/data', methods=['POST'])
def receive_data():
    """Create a new item"""
    try:
        data = request.get_json()
        if not data or 'choice' not in data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        new_entry = [data['choice'], data['situation'][0], data['situation'][1], data['situation'][2], data['situation'][3], data['situation'][4]]

        writeToCSV(new_entry)

        """MAKE CALL TO MODEL HERE"""
        
        x = np.array(data['situation'][:5])
        x_reshaped = x.reshape(1, -1)  # 1 row, 5 features
        print('array: ', x)

        transformed_data = poly.fit_transform(x_reshaped)
        print('written: ', transformed_data)
        prediction = model.predict(transformed_data, batch_size=None, verbose="auto", steps=None, callbacks=None)
        prediction = prediction.flatten()
        print('prediction: ', prediction)

        return jsonify({'prediction': prediction.tolist()}), 201
    
    except Exception as e:
        logger.error(f"Error recieving data: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)