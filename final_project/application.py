from flask import Flask, render_template, request
from cs50 import SQL

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
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""
    return render_template("register.html")

@app.route("/users", methods=["GET", "POST"])
def users():
    """Display registered users for debugging"""
    rows = db.execute("SELECT * FROM users")
    return render_template("users.html", rows=rows)