from flask import Flask, render_template, request, redirect
from database import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Replace with your desired database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
            return render_template('dashboard.html', username=username)
        else:
            error_message = 'Invalid username or password'
            return render_template('login.html', error_message=error_message)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect('/')  # Redirect to the login page after successful registration

    return render_template('registration.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
