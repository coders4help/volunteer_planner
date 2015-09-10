# volunteer_planner
This repro hosts the code for volunteer-planner.org. A platform to schedule shifts of volunteers.

## Please do pull request against the development branch.
If you have questions concerning our workflow please look here
https://github.com/volunteer-planner/volunteer_planner/wiki/DevelopmentRules

## Setup (Ubuntu 14.04)

1.  Install all required Ubuntu packages
    `apt-get install libmysqlclient-dev mysql-client mysql-server python-dev python-pip git`.
    This will install MySQL server, Python libraries and Git. It will ask you to set a root password [ROOT_PASSWORD]
    for the mysql server, if you haven't already set up MySQL in the past. Remember the password.
2.  Clone the repository: `git clone https://github.com/volunteer-planner/volunteer_planner.git`.
    An instance of the volunteer_planner will be created in the folder `volunteer_planner`
3.  Navigate to that folder `cd volunteer_planner`
4.  Create a virtual environment by running `virtualenv --no-site-packages volunteer_planner-venv`
5.  Enable the virtual environment by running `source volunteer_planner-venv/bin/activate` (for bash) or
    `. volunteer_planner-venv/bin/activate.fish` (for fish)
6.  Install all requirements by running `pip install -r requirements/dev.txt`
7.  Enter the volunteer_planner dir (`cd volunteer_planner`).
8.  Copy man.py to manlocal.py (`cp man.py manlocal.py`).
9.  Create a mysql database with the name volunteer_planner with access for user [USERNAME] with password [PASSWORD],
    by entering mysql:

    `mysql -u root -p`
    `"create database volunteer_planner;`
    `grant all privileges on volunteer_planner.* to [USERNAME] identified by '[PASSWORD]';`
    `\q"`

    Enter [ROOT_PASSWORD] from step 1, when asked.
10. Open manlocal.py and fill in [USERNAME], [PASSWORD] for MySQL connection as well as an email address
    (has to be gmail) plus the corresponding gmail password in the appropriate places in that file.
11. Create the database schema by running `./manlocal.py migrate`
12. Add a superuser `./manlocal.py createsuperuser`. Save username and password.
13. Run the server by running `./manlocal.py runserver`
14. Log in with the superuser's credentials
15. To add new organizations and shifts, you have to access the backend at `127.0.0.1:8000/admin`
    (you are logged in as superuser)

## The Project

We use less for precompiling css. The less file you will find in scheduler/static/bootstrap/less/project.less

To make this work you can just initialize the folder with "npm install -g" and then let grunt watch for changes.
