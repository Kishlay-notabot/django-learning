import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import pytz
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kyubechal'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'  # New configuration for upload folder

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the IST time zone
ist = pytz.timezone('Asia/Kolkata')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(10), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(ist))

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(ist))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == '1234':
            session['user'] = 'O'
            return redirect(url_for('chat'))
        elif password == 'asdf':
            session['user'] = 'K'
            return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat', methods=['GET'])
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))

    messages = Message.query.order_by(Message.timestamp).all()
    return render_template('chat.html', messages=messages, user=session['user'])

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user' not in session:
        return redirect(url_for('login'))

    content = request.form.get('message')
    if content:
        message = Message(user=session['user'], content=content)
        db.session.add(message)
        db.session.commit()

    return redirect(url_for('chat'))

@app.route('/images', methods=['GET'])
def images():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    images = Image.query.order_by(Image.timestamp.desc()).all()
    return render_template('images.html', images=images, user=session['user'])

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        new_image = Image(filename=filename, content_type=file.content_type)
        db.session.add(new_image)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Image uploaded successfully'}), 200

@app.route('/get_images', methods=['GET'])
def get_images():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    images = Image.query.order_by(Image.timestamp.desc()).all()
    image_list = [{
        'id': image.id,
        'filename': image.filename,
        'content_type': image.content_type,
        'timestamp': image.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for image in images]

    return jsonify(image_list)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_folder'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)