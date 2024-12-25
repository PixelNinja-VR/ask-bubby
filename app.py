# app.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Simple message storage (replace with a database in production)
chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    # Here you would integrate with your actual genealogy service/database
    # This is a simple placeholder response
    response = generate_response(user_message)
    
    chat_entry = {
        'user_message': user_message,
        'bot_response': response,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    chat_history.append(chat_entry)
    
    return jsonify({'response': response})

def generate_response(message):
    # Placeholder for your genealogy logic
    # You would replace this with actual genealogy search and response logic
    return f"Thanks for asking about your Jewish family history! I'm here to help research your ancestors."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='216.24.60.0/24', port=port)
