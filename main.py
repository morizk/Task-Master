from flask import Flask, render_template, request, redirect, session
from database import db, User, Topic, Task
from datetime import datetime
import secrets



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Replace with your desired database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = secrets.token_hex(16)

db.init_app(app)

@app.route('/')
def login():
    error_message = None
    return render_template('login.html', error_message=error_message)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id

            return render_template('dashboard.html', username=username)
        else:
            error_message = 'Invalid username or password'
            return render_template('login.html', error_message=error_message)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        print("post ")
        topic_name = request.form['topic']
        task_name = request.form['task_name']
        deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
        importance = float(request.form['importance'])
        related_task_id = request.form['related_task']
        description = request.form['description']
        user_id = session.get('user_id')

        topic = Topic.query.filter_by(name=topic_name).first()
        if not topic:
            topic = Topic( topic_name,importance=importance, user_id=user_id)
            db.session.add(topic)
            db.session.commit()

        task = Task(topic_name,task_name, deadline ,importance, related_task_id,description )
        db.session.add(task)
        db.session.commit()

        return render_template('dashboard.html')

    topics = Topic.query.all()

    return render_template('add_task.html', topics=topics)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect('/')

    return render_template('registration.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
