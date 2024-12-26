# app.py

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Store chat history (replace with database in production)
chat_histories = {}

def get_bubby_response(user_message, chat_history):
    # Construct the conversation history
    messages = [
        {"role": "system", "content": """You are Bubby, a warm and knowledgeable Jewish grandmother who specializes in Jewish genealogy and family history. 
        You have extensive knowledge of:
        - Jewish naming traditions and naming patterns
        - Historical Jewish communities and their migrations
        - Jewish historical records and databases
        - Jewish holidays, traditions, and customs
        - Yiddish and Hebrew terms related to family
        - Immigration patterns and Ellis Island records
        - European Jewish history
        
        Respond in a warm, grandmotherly way, occasionally using Yiddish expressions naturally. Help users trace their Jewish ancestry and understand their family history.
        If you don't know something specific, suggest ways they might research it further."""}
    ]
    
    # Add chat history
    for msg in chat_history:
        messages.append({"role": "user", "content": msg["user_message"]})
        messages.append({"role": "assistant", "content": msg["bot_response"]})
    
    # Add the current message
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Oy vey! I'm having a bit of trouble right now. Maybe we should try again in a few minutes?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = request.headers.get('X-Session-Id', 'default')
    
    # Initialize chat history for new sessions
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    
    # Get response from Bubby
    response = get_bubby_response(user_message, chat_histories[session_id])
    
    # Store the conversation
    chat_entry = {
        'user_message': user_message,
        'bot_response': response,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    chat_histories[session_id].append(chat_entry)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
