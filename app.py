from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user, UserMixin
)
from werkzeug.security import generate_password_hash, check_password_hash
import os
from openai import OpenAI

# App setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-this')  # Change this for production!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use Postgres/MySQL for production

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create the database tables
with app.app_context():
    db.create_all()

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered!"}), 201

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Logged in!"})
    return jsonify({"error": "Invalid credentials"}), 401

# Logout endpoint
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out!"})

# Prompt endpoint (requires login)
@app.route('/prompt', methods=['POST'])
@login_required
def prompt():
    data = request.get_json()
    user_prompt = data.get('prompt', '').lower()
    action = ""
    robot_done = ""

    # Always try OpenAI call first
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert video editing assistant. Translate user commands into short, clear video editor actions (like 'Splitting the video.')"},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=24,
            temperature=0
        )
        action = completion.choices[0].message.content.strip()
        robot_done = f"Pretend: {action}"
        print(robot_done)
        return jsonify({'response': action, 'robot': robot_done})
    except Exception as e:
        print(f"OpenAI Error: {e}")
        # FALLBACK: simple command matching below

    if "split" in user_prompt:
        action = "Splitting the video."
        robot_done = "Pretend: Pressing shortcut to split."
        print(robot_done)
    elif "fade" in user_prompt:
        action = "Adding a fade effect."
        robot_done = "Pretend: Moving mouse to apply fade."
        print(robot_done)
    elif "zoom" in user_prompt:
        action = "Applying slow zoom."
        robot_done = "Pretend: Clicking on zoom controls."
        print(robot_done)
    else:
        action = "Sorry, I don't know that command yet."
        robot_done = ""
    return jsonify({'response': action, 'robot': robot_done})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
