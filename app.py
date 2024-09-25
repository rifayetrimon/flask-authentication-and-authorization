from flask import Flask, flash, render_template, request, redirect, session, url_for
from forms import RegistrationForm, LoginForm
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Correctly define the MONGO_URI as a string
app.config["MONGO_URI"] = "mongodb+srv://flask_curd:vkXLEwIoRkT0If6O@cluster0.5jv2s.mongodb.net/flaskDB?retryWrites=true&w=majority"
app.config['SECRET_KEY'] = 'mysecretkey'
mongo = PyMongo(app) 

# Accessing the specified database
db = mongo.db  # This will use the database specified in the URI (flaskDB)

@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if request.method == 'POST':
        data = request.form

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')  # Fixed the spelling here

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('registration'))
        
        # Hash the password before storing it

        hash_password =generate_password_hash(password)

        # Inserting data into the 'users' collection
        db.users.insert_one({
            'username': username,
            'email': email,
            'password': hash_password
        })

        flash('Registration successful!', 'success')
        return redirect(url_for('registration'))  # Redirect to avoid re-su, submission

    return render_template("register.html", form=form, show_navbar=False)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        data = request.form
        
        email = data.get('email')
        password = data.get('password')

        user = db.users.find_one({'email': email, 'password': password})

        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to home after successful login
        else:
            flash('Invalid email or password', 'error')
        
    return render_template("login.html", form=form, show_navbar=False)



@app.route('/home')
def home():
    return render_template('home.html')













if __name__ == "__main__":
    app.run(debug=True)
