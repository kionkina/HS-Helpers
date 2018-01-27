from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import user
from util import db

app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route('/', methods=['GET', 'POST'])
def index():
    if "username" in session:
        return redirect(url_for("HS_homepage"))
    return redirect(url_for("signup"))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if "username" not in session:
        return render_template("signup.html")
    else:
        flash("You're already logged in!")
        return redirect(url_for("HS_homepage"))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if "username" not in session:
        return render_template("signin.html")
    else:
        flash("You're already logged in!")
        return redirect(url_for("HS_homepage"))



@app.route('/HS_homepage', methods = ["GET", "POST"])
def HS_homepage():
    if "username" in session:
        username = session["username"]
        #displays a list of edited stories
        return render_template("HS_homepage.html")
    return redirect(url_for("auth"))

@app.route('/auth', methods = ["GET", "POST"])
def auth():
    #user already logged in
    if "username" in session:
        return redirect(url_for("HS_homepage"))
    if request.method == "GET":
        #user went to /auth without logging in
        return redirect("/")
    try:
        username = request.form['username']
        password = request.form['password']
    except KeyError:
        flash("Please fill out all fields")
        return render_template("signin.html")
    #login authenticated!
    if db.check_credentials(username,password):
        session['username'] = username
        flash("Successfully logged in")
        return redirect(url_for('HS_homepage'))
    else:
        flash("Failed login")
        return redirect(url_for('signin'))

@app.route('/signauth', methods = ["GET", "POST"])
def signauth():
    try:
        #user filled out everything
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
    except KeyError:
        flash("Please fill out all fields")
        return render_template("signup.html")
    if password != password2:
        flash("Passwords don't match")
        return render_template("signup.html")
    if username == "" or password == "" or password2 == "":
        flash("Fields must not be blank")
        return render_template("signup.html")
    if db.add_company(username, password):
        #success! username and password added to database
        flash("Successfully created!")
        return redirect(url_for('signin'))
    else:
        #username couldn't be added to database because it already exists
        flash("Username taken")
        return redirect(url_for('signup'))


@app.route('/logout')
def logout():
    if "username" not in session:
        flash("You aren't logged in")
        return redirect(url_for('signin'))
    session.pop("username")
    flash("You've been logged out")
    return redirect(url_for('index'))



# Passes this variable into every view
@app.context_processor
def logged_in():
    if "username" in session:
        return dict(logged_in=True)
    return dict(logged_in=False)



if __name__ == '__main__':
    app.run(debug=True)
