from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
def home():
    return render_template("index.html")

#this is our sign in page!
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    username = request.get['user']
    password = request.get['pass']

    return render_template("signin.html")

@app.route('/showSignUp')
def showSignUp():
    return render_template("signup.html")

#this is our sign up page!
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':    
        username = request.form['user']
        password = request.form['pass']
        name = request.form['name']
        email = request.form['email']
        print("cheesecake")
        print(name)
        #creating a database for new user
        new_user = Todo(username=username, password=password, name=name, email=email)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('signin'))

        except:
            return ("There was an issue adding this user plus YOU SUCK ")
    return render_template("signin.html")
  
@app.route('/dashboard')
def dashboard():
    return ""

@app.route('/enter_meal', methods=['POST','GET'])
def enter_meal():

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return ("There was an issue adding your task")
    
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('enter_meal.html', meal=tasks)



@app.route('/enter_water', methods=['POST','GET'])
def enter_water():
    return ""

@app.route('/view_progress', methods=['POST','GET'])
def view_progress():
    return ""















@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return 'There was a problem deleting that food item.'


@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):

    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        
        except:
            return 'There was an issue updating your task!'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)