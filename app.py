from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if "username" in session:
        return redirect(url_for("HS_homepage"))
    return render_template("login")


@app.route('signup', methods=['GET', 'POST'])
def signup():
    if "username" not in session:
        return render_template("signup.html")
    else:
        flash("You're already logged in silly")
        return redirect(url_for("HS_homepage"))

if __name__ == '__main__':
    app.run(debug=True)
