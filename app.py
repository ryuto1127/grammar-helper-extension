from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

# Fetch the API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("No OpenAI API key provided. Set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/explain', methods=['POST'])
def explain():
    data = request.get_json()
    sentence = data['text']
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a language assistant for non native English speakers."},
                {"role": "user", "content": f"explain this sentence using simple English: '{sentence}'. At the end of the explanation, add meanings of the words in the sentence which are not common."}
            ]
        )
        explanation = response.choices[0].message.content.strip()
        return jsonify({"explanation": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
