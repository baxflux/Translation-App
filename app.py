from flask import Flask, request, jsonify, render_template
from model_loader import load_model
from translator import translate_text

# Khởi tạo Flask
app = Flask(__name__)

# Load model và tokenizer (được tách riêng trong model_loader)
model, tokenizer = load_model()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No input text provided"}), 400

    translation = translate_text(text, model, tokenizer)
    return jsonify({"translation": translation})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
