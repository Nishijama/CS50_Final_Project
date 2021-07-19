from flask import Flask, render_template, request, redirect, session
from cs50 import SQL
from tempfile import mkdtemp
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from flask_session import Session
from functools import wraps
from hash import make_pw_hash, check_pw_hash


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

db = SQL("sqlite:///database.db")
class User(object):
    def __init__(self, id, requests_stats, pages_stats, shifts, tasks):
        self.id = id
        self.requests_stats = requests_stats
        self.pages_stats = pages_stats
        self.shifts = shifts
        self.tasks = tasks


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user = session["user_id"]
    if request.method == "GET":

        date_query = date.today()
        user_id = session["user_id"]
        requests_query = db.execute("SELECT requests FROM stats WHERE user_id = ? AND date = ?", user_id, date_query)
        pages_query = db.execute("SELECT pages from stats WHERE user_id = ? AND date = ?", user_id, date_query)
        shifts_query = db.execute("SELECT * FROM shifts WHERE user_id = ? AND date = ?", user_id, date_query)
        tasks_query = db.execute("SELECT * FROM tasks WHERE user_id = ? AND date = ?", user_id, date_query)

        current_user = User(user_id, requests_query, pages_query, shifts_query, tasks_query)

        print(current_user.id)
        print(current_user.requests_stats)
        print(current_user.pages_stats)
        print(current_user.shifts)
        print(current_user.tasks)
        return render_template("index.html")

    else:
        return render_template("oops!.html")



@app.route("/login", methods=["GET", "POST"])
#https://werkzeug.palletsprojects.com/en/2.0.x/utils/#werkzeug.security.check_password_hash
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE name = ?", request.form.get("Username"))
        print(rows)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("Password")):
            return oops("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
# https://werkzeug.palletsprojects.com/en/2.0.x/utils/#werkzeug.security.check_password_hash
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("Username")
        password = request.form.get("Password")
        confirmation = request.form.get("Confirmation")

        if password != confirmation:
            return oops("Your passwords didn't match")

        existingUsers = db.execute("SELECT name FROM users")
        for row in range(len(existingUsers)):
            if existingUsers[row].get("name") == username:
                return oops("Sorry, this username is taken")

        pwhash = generate_password_hash(password)
        db.execute("INSERT INTO users (name, password_hash) VALUES (:username, :pwhash)", username=username, pwhash=pwhash)
        return redirect("/")

@app.route("/users", methods=["GET", "POST"])
@login_required
def users():
    """Display registered users for debugging"""
    rows = db.execute("SELECT * FROM users")
    return render_template("users.html", rows=rows)

def oops(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("oops!.html", top=code, bottom=escape(message)), code

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return oops(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
