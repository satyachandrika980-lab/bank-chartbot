from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure API key securely (set GENAI_API_KEY in your environment)
genai.configure(api_key=os.getenv("AIzaSyDSRD5-yJzFzTeSjC4oZjEKqBV7GGPNA4I"))

# Use a supported model
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    # Wrap user input in the banking assistant prompt
    prompt = f"""
    You are a professional banking customer support assistant.

    Your job is to help users with banking services such as:
    - ATM card issues
    - Online banking
    - Account balance information
    - Loan information
    - Card blocking
    - Password reset

    Rules:
    1. Answer clearly and politely.
    2. Give step-by-step instructions if needed.
    3. Only answer banking related questions.
    4. If the question is not related to banking, say:
       "I can only help with banking related questions."

    User question:
    {user_message}
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        app.logger.exception("Error generating response")
        return jsonify({"error": "Failed to generate response", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)