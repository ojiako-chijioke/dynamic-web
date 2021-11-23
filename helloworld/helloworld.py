from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
 return "Hello World from Python Flask Web Framework!"


@app.route("/about-us/")
def about_us():
 return "We are here to serve you!"


@app.route("/hello/<string:name_to_greet>/")
def hello(name_to_greet):
 return "Hello %s, greetings from Flask Framework!" % name_to_greet


@app.route("/hello2/<string:name_to_greet>/")
def hello2(name_to_greet):
 return render_template('hello.html', person_to_greet=name_to_greet)


@app.route("/hello3/<string:name_to_greet>/")
def hello3(name_to_greet):
 return render_template('hello-with-layout.html', person_to_greet=name_to_greet)


@app.route("/user/<int:id>/")
def show_user(id):
 return "The id passed is {}".format(id)


@app.route("/deposit/<float:amount>/")
def deposit_money(amount):
 return "The amount to deposit is {}".format(amount)


@app.route("/path/<path:subpath>/")
def path(subpath):
 return "The subpath passed in URL is {}".format(subpath)


if __name__ == "__main__":
 app.run()