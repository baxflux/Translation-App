from flask import Blueprint, render_template, request

translate_bp = Blueprint("translate", __name__)

@translate_bp.route("/", methods=["GET", "POST"])
def index():
    source_text = ""
    translation = ""
    max_tokens = 512

    if request.method == "POST":
        source_text = request.form.get("text", "").strip()

        try:
            max_tokens = int(request.form.get("max_tokens", 512))
        except ValueError:
            max_tokens = 512

        max_tokens = min(max_tokens, 1024)

        if source_text:
            from app.services.translator import translate_long_text
            translation = translate_long_text(
                source_text,
                max_tokens=max_tokens
            )

    return render_template(
        "index.html",
        source_text=source_text,
        translation=translation,
        max_tokens=max_tokens
    )
