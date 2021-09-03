from flask import Flask

# If you need setup of flask: set FLASK_APP=app, set FLASK_ENV=development
def create_app():
    app = Flask(__name__)

    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app