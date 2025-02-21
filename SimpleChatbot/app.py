from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

class Chatbot:
    def chat(self, message):
        if not message.strip():
            return "I can't repeat an empty message!"
        return message

chatbot = Chatbot()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_message = request.form.get("text", "").strip()
        bot_response = chatbot.chat(user_message)
        return jsonify({"bot_response": bot_response})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
