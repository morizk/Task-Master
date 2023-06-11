from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    topics = db.relationship('Topic', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Topic(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    importance = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='topic', lazy=True)

    def __init__(self, name, importance, user_id):
        self.name = name
        self.importance = importance
        self.user_id = user_id

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.Text,  nullable=False)
    description = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    topic_name = db.Column(db.Integer, db.ForeignKey('topic.name'), nullable=False)
    related_task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    tasks = db.relationship('Task', backref=db.backref('related_task', remote_side=[id]), lazy=True)
    importance = db.Column(db.Float, nullable=False)

    def __init__(self,topic_name,task_name, deadline ,importance, related_task_id,description ):
        self.importance=importance
        self.task_name=task_name
        self.topic_name=topic_name
        self.description = description
        self.deadline = deadline
        self.related_task_id = related_task_id
