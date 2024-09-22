from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///TODO.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    desc = db.Column(db.String(800), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

quotes = [
    "The only way to do great work is to love what you do. — Steve Jobs",
    "Believe you can and you're halfway there. — Theodore Roosevelt",
    "Your time is limited, don't waste it living someone else's life. — Steve Jobs",
    "The future belongs to those who believe in the beauty of their dreams. — Eleanor Roosevelt",
    "It does not matter how slowly you go as long as you do not stop. — Confucius",
    "Success is not the key to happiness. Happiness is the key to success. — Albert Schweitzer",
    "Don’t watch the clock; do what it does. Keep going. — Sam Levenson",
    "The only limit to our realization of tomorrow will be our doubts of today. — Franklin D. Roosevelt",
    "Act as if what you do makes a difference. It does. — William James",
    "Success is walking from failure to failure with no loss of enthusiasm. — Winston Churchill",
    "What lies behind us and what lies before us are tiny matters compared to what lies within us. — Ralph Waldo Emerson",
    "You miss 100% of the shots you don’t take. — Wayne Gretzky",
    "Hardships often prepare ordinary people for an extraordinary destiny. — C.S. Lewis",
    "The best way to predict the future is to create it. — Peter Drucker",
    "I find that the harder I work, the more luck I seem to have. — Thomas Jefferson",
    "Opportunities don't happen. You create them. — Chris Grosser",
    "Dream big and dare to fail. — Norman Vaughan",
    "Everything you’ve ever wanted is on the other side of fear. — George Addair",
    "If you can dream it, you can achieve it. — Zig Ziglar",
    "It always seems impossible until it’s done. — Nelson Mandela",
    "Limit your 'always' and your 'nevers'. — Amy Poehler",
    "Keep your face always toward the sunshine—and shadows will fall behind you. — Walt Whitman",
    "The way to get started is to quit talking and begin doing. — Walt Disney",
    "You are never too old to set another goal or to dream a new dream. — C.S. Lewis",
    "If you want to lift yourself up, lift up someone else. — Booker T. Washington"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if not title or not desc:
            return "Error: Title and Description cannot be empty"
        new_todo = Todo(title=title, desc=desc)
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')
    
    random_quote = random.choice(quotes)
    allTodo = Todo.query.all()
    return render_template('frontend.html', allTodo=allTodo, random_quote=random_quote)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if not title or not desc:
            return "Error: Title and Description cannot be empty"
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect('/')
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>', methods=['POST'])
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')



