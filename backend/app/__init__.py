from flask import Flask

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    from app.routes.translate import translate_bp
    app.register_blueprint(translate_bp)

    # Load model after server starts (lazy loading on first request)
    @app.before_request
    def ensure_model_loaded():
        from app.services import translator
        if not translator.model_loaded:
            translator.load_model()

    return app
