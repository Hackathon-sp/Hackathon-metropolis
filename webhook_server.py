from flask import Flask, request, jsonify
from reservation import create_reservation
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Middleware to parse JSON
@app.before_request
def handle_json():
    if request.content_type == 'application/json':
        request.json_data = request.get_json()

# Webhook endpoints
@app.route('/test', methods=['POST'])
def test_webhook():
    print('🔔 Webhook received:', request.json)
    return jsonify({'status': 'OK'}), 200

@app.route('/mews-webhook', methods=['POST'])
def mews_webhook():
    data = request.json
    required_params = [
        'locationCode','contactNumber', 'firstName', 'email', 'startAt', 'stopAt'
    ]
    
    # Validate required parameters
    missing_params = [param for param in required_params if param not in data]
    if missing_params:
        return jsonify({
            'error': 'Missing required parameters',
            'missing': missing_params
        }), 400

    try:
        # Call create_reservation with validated parameters
        result = create_reservation(
            location=data['locationCode'],
            contactNumber=data['contactNumber'],
            name=data['firstName'],
            email = data['email'],
            startAt=data['startAt'],
            stopAt=data['stopAt']
        )
        
        if result:
            return jsonify({'status': 'Reservation created', 'data': result}), 200
        else:
            return jsonify({'error': 'Failed to create reservation'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Start server
if __name__ == '__main__':
    PORT =  os.getenv('PORT')
    print(f'Server running on http://localhost:{PORT}')
    app.run(port=PORT)
