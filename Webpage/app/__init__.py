from flask import Flask

# If you need setup of flask: set FLASK_APP=app, set FLASK_ENV=development
def create_app():
    app = Flask(__name__)

    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app

# How to use a FLASK
# 1. Change a bert env of conda.
# 2. Move installed flask path
# 3. Set up FLASK_APP and FLASK_ENV

# How to use a localtunnel
# 1. Open a cmd as a admin mode.
# 2. Change a bert env of conda.
# 3. lt --port 5000 --subdomain *