from flask import Flask, render_template, url_for

app = Flask(__name__, template_folder="./Templates")

@app.route('/')
def home():
    return render_template("home_body.html")

@app.route('/Sign-in')
def sign_in():
    return render_template("sign_in.html")

@app.route('/Sign-up')
def sign_up():
    return render_template("sign_up.html")