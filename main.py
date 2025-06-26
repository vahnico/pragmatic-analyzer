from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return "Pragmatic Analyzer API is running!"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    dialogue = data.get("text")

    prompt = f"""
    You are a pragmatic linguist. Analyze the following dialogue using the Pragmatic Analysis Protocol:
    1. Use Brown and Levinson (context)
    2. Grice’s Maxims (maxim scoring)
    3. Levinson (implicature)
    4. Searle (speech acts)
    5. Brown & Levinson + Culpeper (politeness)
    Analyze line-by-line and give percentage per line and final speaker comparison.

    Dialogue:
    {dialogue}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in pragmatic linguistics using a strict scoring protocol."},
            {"role": "user", "content": prompt}
        ]
    )

    analysis = response['choices'][0]['message']['content']
    return jsonify({"result": analysis})