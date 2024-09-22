from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kyubechal'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the IST time zone
ist = pytz.timezone('Asia/Kolkata')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(10), nullable=False)
    content = db.Column(db.String(200), nullable=False)
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
