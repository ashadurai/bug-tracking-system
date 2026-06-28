from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db
from routes.users import users_bp
from routes.bugs import bugs_bp
from routes.notifications import notifications_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

# Register Blueprints
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(bugs_bp, url_prefix='/api/bugs')
app.register_blueprint(notifications_bp, url_prefix='/api/notifications')

@app.route('/')
def index():
    return {'message': 'Bug Tracking System API is running!', 'status': 'success'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
