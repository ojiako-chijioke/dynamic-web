from flask_sqlalchemy import SQLAlchemy
import models
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bookexampledbpassword@localhost/bookexample'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = b'\xdf\x9c9\\\x99\xe7\x17\xbf\x17\x08m5`\x89~\xda\xe2\xb5(\xe9\xc0\xe24\x8b'

@app.route("/")
def home():
    return render_template('home.html', title="Home")

@app.route("/products-and-services/")
def products_and_services():
    return render_template('products-and-services.html', title="Products and Services")

@app.route("/about-us/")
def about_us():
    return render_template('about-us.html', title="About Us")

@app.route("/signup/")
def signup():
    return render_template('signup.html', title="SIGN UP", information="Use the form displayed to register")

@app.route("/process-signup/", methods=['POST'])
def process_signup():
    # Let's get the request object and extract the parameters sent into local variables.
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    othernames = request.form['othernames']
    email = request.form['email']
    password = request.form['password']
    # let's write to the database.
    try:
        user = models.User(firstname=firstname, lastname=lastname, othernames=othernames, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        # Error caught, prepare error information for return
        information = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('signup.html', title="SIGN-UP", information=information)

    # If we have gotten to this point, it means that database write has been successful. Let us compose success info
    information = 'User by name {} {} successfully added. The login name is the email address {}.'.format(firstname, lastname, email)

    return render_template('signup.html', title="SIGN-UP", information=information)

app.route("/login/")
def login():
    #Save off in session where we should go after login process. Session survives across requests.
    #Where to go is passed as parameter named next along with the request to /login/ URL.
    session['next_url'] = request.args.get('next', '/') #get the next or use default '/' URL after login
    return render_template('login.html', title="SIGN IN", information="Enter login details")

@app.route("/process-login/", methods=['POST'])
def process_login():
    # Get the request object and the parameters sent.
    email = request.form['email']
    password = request.form['password']

    # call our custom defined function to authenticate user
    if (authenticateUser(email,password)):
        session['username'] = email
        session['userroles'] = 'admin' #just hardcoding for the sake of illustration. This should be read from database.
        return redirect(session['next_url'])
    else:
        error = 'Invalid user or password'
        return render_template('login.html', title="SIGN IN", information=error)

def authenticateUser(email, password):
    user = models.User.query.filter_by(email=email).first()
    if user and user.check_password(password):  # return True only if both are true.
        return True
    else:
        return False

def logged_in():
    if 'username' not in session:
        return False
    else:
        return True

@app.route("/no-anonymity-here/")
def no_anonymity_here():
    if not logged_in():
        return redirect(url_for('login', next='/no-anonymity-here/'))
    # username in session, continue
    return '''
    You have successfully entered a non-anonymous zone. You are logged in as {}.
    <a href="/">Click here to go to the Home page</a>
    '''.format(session['username'])

@app.route("/logout/")
def logout():
    session.pop('username', None) # remove the item with key called username from the session
    session.pop('userroles', None) # remove the item with key called userroles from the session
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(port=5001)
# here we are using a different port so as not to conflict with that allocated to our helloworld.py