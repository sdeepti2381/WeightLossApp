from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
engine = create_engine('sqlite:///user.db', echo=True)
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/showSignIn')
def showSignIn():
    return render_template("signin.html")


#this is our sign in page!
@app.route('/signin', methods = ["GET","POST"])
def signin():  

    if request.method == "POST":

        username = str(request.form.get('username'))
        password = str(request.form.get('password'))
        print("test") 
        print(username)
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(users).filter(users.username.in_([username]), users.password.in_([password]) )
        result = query.first()
        if result:
            result_name = result.name
            return render_template("dashboard.html", name=result_name)
        else:
            return "Object not found " + username + " " + password


@app.route('/showSignUp')
def showSignUp():
    return render_template("signup.html")

#this is our sign up page!
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':    
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        email = request.form.get('email')

        #creating a database for new user
        new_user = users(username=username, password=password, name=name, email=email)
        print(username)
        print(name)
        print(password)
        print(email)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('showSignIn'))

        except:
            return ("There was an issue adding this user")
    return render_template("signin.html")
  
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/enter_meal', methods=['POST','GET'])
def enter_meal():

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = todo(content=task_content)

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