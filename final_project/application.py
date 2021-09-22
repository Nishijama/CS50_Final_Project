from flask import Flask, render_template, request, redirect, session
from cs50 import SQL
from tempfile import mkdtemp
from calendar import monthrange
from datetime import timedelta, date
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

# Global Variables here:
today = date.today()
year = today.year
current_month = today.strftime("%m")
landing_page = "/?month=" + current_month


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    user_id = session["user_id"]
    month = str(request.args.get("month"))
    first_of_month = (str(year) + '-' + month + '-01',)
    last_of_month = (str(year) + '-' + month + '-31',)

    # Define GET request
    if request.method == "GET":
        #Perform necessary SQL queries
        statisticsQuery = db.execute("SELECT * FROM statistics WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date", user_id, first_of_month, last_of_month)
        topStatQuery = db.execute("Select SUM(requests) AS rTotal, ROUND(AVG(requests),2) AS rAverage, SUM(pages) AS pTotal, ROUND(AVG(pages),2) AS pAverage FROM statistics WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date", user_id, first_of_month, last_of_month)
        shiftsQuery = db.execute("SELECT COUNT(user_id), shift FROM statistics WHERE shift IS NOT NULL AND user_id = ? AND date BETWEEN ? AND ? GROUP BY shift", user_id, first_of_month, last_of_month)
        tasksQuery = db.execute("SELECT COUNT(user_id), task FROM statistics WHERE task IS NOT NULL AND user_id = ? AND date BETWEEN ? AND ? GROUP BY task", user_id, first_of_month, last_of_month)
        print(topStatQuery)

        # Handle data for Top Stats
        for row in topStatQuery:

            topStatReqTotal = row["rTotal"]
            if topStatReqTotal == None:
                topStatReqTotal = 0
            print(topStatReqTotal)

            topStatReqAvg = row["rAverage"]
            if topStatReqAvg == None:
                topStatReqAvg = 0.0
            print(topStatReqAvg)

            topStatPageTotal = row["pTotal"]
            if topStatPageTotal == None:
                topStatPageTotal = 0

            topStatPageAvg = row["pAverage"]
            if topStatPageAvg == None:
                topStatPageAvg = 0.0
                return render_template("empty_index.html",month=month, year=year)

        # Handle data for charts
        statistics_chart_requests_data = [ ['Day', 'Requests'] ]
        for row in statisticsQuery:
            statistics_chart_requests_data.extend([[row["date"][-2:], row["requests"]]])

        statistics_chart_pages_data = [ ['Day', 'Pages'] ]
        for row in statisticsQuery:
            statistics_chart_pages_data.extend([ [row["date"][-2:], row["pages"]] ])

        tasks_chart_data = []
        for row in tasksQuery:
            tasks_chart_data.extend([[row["task"], row["COUNT(user_id)"]]])

        shifts_chart_data = []
        for row in shiftsQuery:
            shifts_chart_data.extend([[row["shift"], row["COUNT(user_id)"]]])

        # Return template
        return render_template("index.html", statisticsQuery=statisticsQuery, topStatQuery=topStatQuery, shiftsQuery=shiftsQuery,
                                             tasksQuery=tasksQuery, month=month, year=year, statistics_chart_requests_data=statistics_chart_requests_data,
                                             statistics_chart_pages_data=statistics_chart_pages_data, tasks_chart_data=tasks_chart_data,
                                             shifts_chart_data=shifts_chart_data, topStatReqTotal=topStatReqTotal, topStatReqAvg=topStatReqAvg,
                                             topStatPageTotal=topStatPageTotal, topStatPageAvg=topStatPageAvg)

    # Define POST request
    elif request.method == "POST":
        month = str(request.args.get("month"))

        # Define Add POST request
        if "AddRecordsButton" in request.form:
            date_var = request.form.get("date")
            requests = request.form.get("requests")
            pages = request.form.get("pages")
            shift = request.form.get("shift")
            task = request.form.get("task")
            month = date_var[5:7]
            first_of_month = (str(year) + '-' + month + '-01',)
            last_of_month = (str(year) + '-' + month + str(monthrange(year, int(month))[1]))

            # Check if there are already any entries for given month for this user
            check_stats = db.execute("SELECT requests FROM statistics WHERE user_id = ? AND date BETWEEN ? AND ?", user_id, first_of_month, last_of_month)
            # If there are no entries this month, create empty row for every day this month
            if len(check_stats) == 0:
                # create an empty row for each day this year for the new user
                # https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-50.php
                # https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
                def daterange(date1, date2):
                    for n in range(int ((date2 - date1).days)+1):
                        yield date1 + timedelta(n)

                start_date = date(year, int(month), 1)
                end_date = date(year, int(month), monthrange(year, int(month))[1])

                for dt in daterange(start_date, end_date):
                    single_date = dt.strftime("%Y-%m-%d")
                    print(single_date)
                    db.execute("INSERT INTO statistics (user_id, date, requests, pages, shift, task) VALUES (:user_id, :date, NULL, NULL, NULL, NULL)",user_id = user_id, date=single_date)

            # Update given date with new records
            db.execute("UPDATE statistics SET requests = ?, pages = ?, shift = ?, task = ? WHERE user_id = ? AND date = ?", requests, pages, shift, task, user_id, date_var)

        # Define Remove POST request
        elif "RemoveRecordsButton" in request.form:
            deleteQuery = request.form.get("records")
            #Select records to delete
            check_stats = db.execute("SELECT requests FROM statistics WHERE user_id = ? AND date = ?", user_id, deleteQuery[:10])
            #Overwrite the records with NULL values
            if len(check_stats) != 0:
                db.execute("UPDATE statistics SET requests = NULL, pages = NULL, shift = NULL, task = NULL WHERE user_id = ? AND date = ?", user_id, deleteQuery[:10])

        # Update content on the page and display as per GET request
        # Perform necessary SQL queries
        statisticsQuery = db.execute("SELECT * FROM statistics WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date", user_id, first_of_month, last_of_month)
        topStatQuery = db.execute("Select SUM(requests) AS rTotal, ROUND(AVG(requests),2) AS rAverage, SUM(pages) AS pTotal, ROUND(AVG(pages),2) AS pAverage FROM statistics WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date", user_id, first_of_month, last_of_month)
        shiftsQuery = db.execute("SELECT COUNT(user_id), shift FROM statistics WHERE shift IS NOT NULL AND user_id = ? AND date BETWEEN ? AND ? GROUP BY shift", user_id, first_of_month, last_of_month)
        tasksQuery = db.execute("SELECT COUNT(user_id), task FROM statistics WHERE task IS NOT NULL AND user_id = ? AND date BETWEEN ? AND ? GROUP BY task", user_id, first_of_month, last_of_month)

        # Handle data for Top Stats
        for row in topStatQuery:

            topStatReqTotal = row["rTotal"]
            if topStatReqTotal == None:
                topStatReqTotal = 0
            print(topStatReqTotal)

            topStatReqAvg = row["rAverage"]
            if topStatReqAvg == None:
                topStatReqAvg = 0.0
            print(topStatReqAvg)

            topStatPageTotal = row["pTotal"]
            if topStatPageTotal == None:
                topStatPageTotal = 0

            topStatPageAvg = row["pAverage"]
            if topStatPageAvg == None:
                topStatPageAvg = 0.0
                return render_template("empty_index.html",month=month, year=year)

        # andle data for charts
        statistics_chart_requests_data = [ ['Day', 'Requests'] ]
        for row in statisticsQuery:
            statistics_chart_requests_data.extend([[row["date"][-2:], row["requests"]]])

        statistics_chart_pages_data = [ ['Day', 'Pages'] ]
        for row in statisticsQuery:
            statistics_chart_pages_data.extend([[row["date"][-2:], row["pages"]]])

        tasks_chart_data = []
        for row in tasksQuery:
            tasks_chart_data.extend([[row["task"], row["COUNT(user_id)"]]])

        shifts_chart_data = []
        for row in shiftsQuery:
            shifts_chart_data.extend([[row["shift"], row["COUNT(user_id)"]]])

        chart_data = [ ['Day', 'Requests', 'Pages'] ]
        for row in statisticsQuery:
            chart_data.extend([[row["date"][-2:], row["requests"], row["pages"]]])

        # Return template
        return render_template("index.html", statisticsQuery=statisticsQuery, topStatQuery=topStatQuery, shiftsQuery=shiftsQuery, tasksQuery=tasksQuery,year=year, month=month,
                                             statistics_chart_requests_data=statistics_chart_requests_data, statistics_chart_pages_data=statistics_chart_pages_data,
                                             tasks_chart_data=tasks_chart_data, shifts_chart_data=shifts_chart_data, topStatReqTotal=topStatReqTotal,
                                             topStatReqAvg=topStatReqAvg, topStatPageTotal=topStatPageTotal, topStatPageAvg=topStatPageAvg)

@app.route("/login", methods=["GET", "POST"])
#https://werkzeug.palletsprojects.com/en/2.0.x/utils/#werkzeug.security.check_password_hash
def login():

    # Forget any user_id
    session.clear()

    # Define POST request
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
        return redirect(landing_page)

    # Define GET request
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
# https://werkzeug.palletsprojects.com/en/2.0.x/utils/#werkzeug.security.check_password_hash
def register():

    # Define GET request
    if request.method == "GET":
        return render_template("register.html")

    # Define POST request
    else:
        # Get and check input from the user
        username = request.form.get("Username")
        password = request.form.get("Password")
        confirmation = request.form.get("Confirmation")

        # Check if password matches the confirmation
        if password != confirmation:
            return oops("Your passwords didn't match")

        # Check if username is available
        existingUsers = db.execute("SELECT name FROM users")
        for row in range(len(existingUsers)):
            if existingUsers[row].get("name") == username:
                return oops("Sorry, this username is taken")

        # Generate password hash and add the user to the database
        pwhash = generate_password_hash(password)
        db.execute( "INSERT INTO users (name, password_hash) "
                    "VALUES (:username, :pwhash)", username=username, pwhash=pwhash)

        # Remember which user has logged in
        current_user = db.execute("SELECT * FROM users WHERE name = ?", request.form.get("Username"))
        session["user_id"] = current_user[0]["id"]

        return redirect(landing_page)

@app.route("/landscape", methods=["GET"])
@login_required
def landscape():

    user_id = session["user_id"]
    # Prepare dates
    month = str(request.args.get("month"))
    first_of_month = (str(year) + '-' + month + '-01')
    last_of_month = (str(year) + '-' + month + str(monthrange(year, int(month))[1]))

    # Query database for data for charts
    landscapeQuery = db.execute("SELECT users.id, users.name, SUM(statistics.requests) AS rTotal, "
                                "ROUND(AVG(statistics.requests), 2) AS rAverage, SUM(statistics.pages) AS pTotal, "
                                "ROUND(AVG(statistics.pages), 2) AS pAverage "
                                "FROM users "
                                "LEFT OUTER JOIN statistics ON statistics.user_id = users.id "
                                "AND statistics.date BETWEEN ? AND ? "
                                "GROUP BY users.id "
                                "ORDER BY rTotal ", first_of_month, last_of_month)
    print(type(landscapeQuery))
    print(landscapeQuery)
    # Prepare data for the charts
    landscape_chart_data = [ ['User', 'Requests', 'Pages'] ]
    average_chart_data = [ ['User', 'Requests', 'Pages'] ]

    for row in landscapeQuery:
        if row["id"] == user_id:
            landscape_chart_data.extend([[row["name"], row["rTotal"], row["pTotal"]]])
            average_chart_data.extend([[row["name"], row["rAverage"], row["pAverage"]]])
        else:
            landscape_chart_data.extend([[" ", row["rTotal"], row["pTotal"]]])
            average_chart_data.extend([[" ", row["rAverage"], row["pAverage"]]])

    # Return template
    return render_template("landscape.html", month=month, landscapeQuery=landscapeQuery,
                            landscape_chart_data=landscape_chart_data, average_chart_data=average_chart_data)

@app.route("/users", methods=["GET", "POST"])
@login_required
def users():
    # Display registered users for debugging
    rows = db.execute("SELECT * FROM users")
    return render_template("users.html", rows=rows)

def oops(message, code=400):
    # Render message with an apropriate appology to the user
    return render_template("oops!.html", code=code, message=message), code

def errorhandler(e):
    # Handle error
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return oops(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
