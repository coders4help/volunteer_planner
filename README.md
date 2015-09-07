# volunteer_planner
This repro hosts the code for volunteer-planner.org. A platform to schedule shifts of volunteers.


## Setup (Ubuntu 14.04)

1. Install new Ubuntu packages `apt-get install libmysqlclient-dev mysql-client mysql-server`. It will ask you to set a root password [ROOT_PASSWORD] for the mysql server. Remember the password.
2. Create a virtual environment by running `virtualenv --no-site-packages volunteer_planner-venv`
3. Enable the virtual environment by running `source volunteer_planner-venv/bin/activate`
4. Install all requirements by running `pip install -r requirements/dev.txt`
5. Enter the volunteer_planner dir.
6. Copy man.py to manlocal.py.
7. Create a mysql database with the name volunteer_planner with access for user [USERNAME] with password [PASSWORD], by entering mysql: `mysql -u root -p[ROOT_PASSWORD]`
8. Tyep the followign commands within the MySQL session
  1. `create database volunteer_planner;`
  2. `grant all privileges on volunteer_planner to [USERNAME] identified by '[PASSWORD]';`
  3. `\q`
9. Copy man.py to manlocal.py and fill in [USERNAME], [PASSWORD]  as well as an email address (has to be gmail) the corresponding gmail password in the appropriate places in that file.
10. Run the server by running `./manlocal.py runserver`
