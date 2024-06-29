import uuid
from flask import Flask, request, jsonify, render_template
import cohere
from cohere import ChatMessage


app = Flask(__name__)

# Initialize Cohere client
co = cohere.Client('T7E5YdqYVduosUnRrTAGvimDFbrSXFSdUOmk3nHA')  # Replace with your actual API key

# Define the reference text
reference_text = """
This webpage provides transaction details for a successful transaction on the Solana blockchain. The transaction occurred approximately one minute ago, at 7:44 PM UTC on June 28, 2024. The signer of the transaction was "26cnPXNAAFs1oGuFpsgnjbB4ym9YkcMMdd7Z48hr5yyY", and the fee for the transaction was 0.000005. The transaction version is listed as "legacy", and the previous block hash is given as "FHWbRLu5tfsdEPcBNpzxmc6hN1P43wAXxJW9mnjpdrrq". The notes and instruction details for the transaction are not provided in the summary. The balance changes for the addresses involved in the transaction are listed, with no change in SOL balance for the signer address and a small decrease in SOL balance for the fee payer address. The token balance change is not applicable for this transaction, as indicated by the "No data" entry.
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