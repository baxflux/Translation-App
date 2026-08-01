from flask import Blueprint, render_template, request, jsonify
import json

translate_bp = Blueprint("translate", __name__)

@translate_bp.route("/", methods=["GET", "POST"])
def index():
    source_text = ""
    translation = ""
    duration = 0
    
    if request.method == "POST":
        source_text = request.form.get("text", "").strip()

        if source_text:
            from app.services.translator import translate_long_text
            translation, duration = translate_long_text(source_text)

    return render_template(
        "index.html",
        source_text=source_text,
        translation=translation,
        duration=duration
    )
