import uuid
from flask import Flask, request, jsonify, render_template
import cohere
from cohere import ChatMessage


app = Flask(__name__)

# Initialize Cohere client
co = cohere.Client('T7E5YdqYVduosUnRrTAGvimDFbrSXFSdUOmk3nHA')  

# Define the reference text
reference_text = """
The webpage provides information about the USD Coin (USDC) token on the Jupiter platform. The token has a current price of $1.00, a market cap of $32.3 billion, and a 24-hour volume of $2.8 billion. The webpage also includes details such as the current supply, decimals, mint authority, freeze authority, token extension, and owner. It provides a list of recent transactions, metadata, pools, and distribution information. The status of the transactions is indicated as "Success," and the transaction details include the transaction hash, method, block, age, instructions, value, transaction fee, and tokens involved. The webpage also includes links to explore more features and tools on the Jupiter platform.
"""

# Define the preamble
preamble = f"""
You are an AI assistant integrated with Solana blockchain explorers. Provide user-friendly, intuitive explanations of account activities, transactions, and program interactions using Program's Interface Description Language (IDL). Avoid greetings.

Reference Text:
{reference_text}
"""

# Initialize the chat history
chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    # Chatbot response
    stream = co.chat_stream(message=user_message,
                            model="command-r-plus",
                            preamble=preamble,
                            chat_history=chat_history)

    chatbot_response = ""
    for event in stream:
        if event.event_type == "text-generation":
            chatbot_response += event.text

    # Add to chat history
    chat_history.extend(
        [ChatMessage(role="USER", message=user_message),
         ChatMessage(role="CHATBOT", message=chatbot_response)]
    )
    
    return jsonify({"response": chatbot_response})

if __name__ == '__main__':
    app.run(debug=True)