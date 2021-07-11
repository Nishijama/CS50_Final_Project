from flask import Flask, render_template, request
from cs50 import SQL
from hash import make_pw_hash, check_pw_hash


app = Flask(__name__)
db = SQL("sqlite:///database.db")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return render_template("index.html")
    if request.method == "GET":
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "GET":
        return render_template("login.html")
    else:
        # check if user exists, check if pw is correct, redirect to the main page
        return 0


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user""" 
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("name")
        password = request.form.get("password")

        #here we will hash the password
        password_hash = make_pw_hash(password)
        #
        #

        db.execute("INSERT INTO users (name, password_hash) VALUES(:name, :password_hash)", name = name, password_hash = password_hash)

@app.route("/users", methods=["GET", "POST"])
def users():
    """Display registered users for debugging"""
    rows = db.execute("SELECT * FROM users")
    return render_template("users.html", rows=rows)