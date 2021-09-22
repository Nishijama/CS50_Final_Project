# Personal Dashboard App
#### Video Demo:  <URL HERE>
#### Description:
I developped this app with my current job in mind and I even hope I can get it hosted on our Intranet so that it's put to an actual use.
I work as a workflow planner in a Visual Graphics Department and our main task as planners is managing incoming requests.
I work in a mid-sized team and our individual productivity is assessed in part based on the number of requests and pages we process every day.
Currently, there is no convenient way for us to track these numbers, and we have no idea how we are doing in relation to other teammates.
I’ve come up with this app to make tracking of the numbers easy and to allow for comparison between peers.

#### Implementation
I set up the application using Flask framework to manage different routes and allow for communication with a SQLite database.
The heart of the app is the application.py file. It contains 5 routes: /register, /login, /, /landsacpe and /users.
The register and login routes are self-explanatory and are havily leaning on the code provided by the CS50 for the 'Finance'
project (including the separate hash.py file that handles hashing and retreving hashed passwords).
The users route is not accessible through any on-page link. It's there to conveniently check what users are registered on
the page for administrative purposes.

The / route and the corresponding templates: index.html and index_empty.html are where
I put the most time and effort as this is the homepage for my application. Here the python code handles the GET request that prints
the dashboard to the screen and two different POST requests depending on whether the user adds new records to the page or deletes
existing records. Each request has its own SQLite queeries that allow for manipulating data on the page. Here I faced a interesting
design choice: the home page displays monthly statistics. So, at the top of the page you can choose a month you want to see and
appropriate data will be fetched from the database and the table and charts will be populated accordingly. I struggled to come up
with a good logic that handles the fact that if user inserts a sigle day, somehow we need to show that in context of the whole month.
After playing around with an idea to create empty rows with just dates for every day of the year for a new user upon registration,
I figured that the database will grow beyond any reason as soon as new users start registering. So after some more thought I decided
that when the user adds a new record, the app will query the database to check if there are any records for this user for this month.
If it's a first date in that month, the app will then create a new row for every day in that month with just the dayte and NULL values
(the app is using a calendar module to determine how many days given month in a given year has). If there are already records for that
month, the program will update the values for the date provided by the user - overwriting NULL values, or updating previously provided
values. Similarly, when the user wants to delete records and displays the window, the app will query the database for every date that has
non-NULL values and the user's ID and return them to the user in the form. When they choose record to delete and submit, the app
updates values for that date with NULL values.

Another interesting thing I learnt while working on the app is using the Google Chart API and manipulating it's propertiess using JavaScript
and preparing and transporting its data using JSON.

There other route is called /Landscape. This subpage, allows to view the user's statistics in comparison to the other users.
It’s basically a ranking, but with a degree of anonymity, as one cannot see the names of other users by their data.
I implemented this at the python level - while preparing data for the JSON file, the app replaced all usernames from the database,
except for the logged-in user with empty strings. This way, every team member retains their privacy, but the user can see how they perform compared to others.


The project contains a total of 9 jinja templates including 2 different layouts that the remaining templates extend. There are also 4 CSS files - one
master style and the others that specify styles of specific subpages.
While I tinkered with separate JS files for a while, I ended up embedding the JavaScript code inside respective HTML files to avoid load delays in the
Google Charts.

Finally, I made the pages responsive, so that the layout and certain details change to accommodate for a vertical orientation and a smaller screen.





