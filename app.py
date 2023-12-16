# import streamlit as st
# from utils import get_answer

# # Title and instructions
# st.title("Langchain Chatbot")
# st.write("Ask me anything!")

# # User input and chatbot response
# user_query = st.text_input("Your question:")
# if user_query:
#     chatbot_response = get_answer(user_query)
#     st.write(f"Chatbot: {chatbot_response}")

# Install required packages

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import streamlit as st

# Your existing functions
def process_llm_response(llm_response):
    ans1 = ""
    ans1 += llm_response['result']
    ans1 += '\n\nSources:'
    for source in llm_response['source_documents']:
        ans1 += "Page number - "+str(source.metadata['page'])+" "+source.metadata['source']
    return ans1

def final_func(Query):
    ans = process_llm_response(qa_chain(Query))  # Assuming qa_chain is defined somewhere
    return ans

# Flask application
app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when the app is run

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    query = data.get('query', '')
    response = final_func(query)
    return jsonify({'response': response})

# Streamlit app
def main():
    st.title("LangChain Model Interface")

    # Input query from the user
    query = st.text_area("Enter your query:")

    # Send query to Flask API
    if st.button("Get Response"):
        response = get_flask_response(query)
        st.text("Response:")
        st.text(response)

def get_flask_response(query):
    # Send query to Flask API and get the response
    import requests
    api_url = "http://127.0.0.1:5000/api"  # Use the ngrok URL if running on Colab
    data = {'query': query}
    response = requests.post(api_url, json=data)
    return response.json().get('response', '')

# Run the Streamlit app
if __name__ == '__main__':
    app.run()
