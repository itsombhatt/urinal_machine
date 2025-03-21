from flask import Flask, request, jsonify
import logging
import csv

from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data = []

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
        prediction = 1;

        return jsonify({'prediction': prediction}), 201
    
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