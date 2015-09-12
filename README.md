# volunteer_planner
This repro hosts the code for volunteer-planner.org. A platform to schedule shifts of volunteers.

## Please do pull request against the development branch.
If you have questions concerning our workflow please look here
https://github.com/volunteer-planner/volunteer_planner/wiki/DevelopmentRules

## Setup (Ubuntu 14.04)

### 1.Install all required Ubuntu packages

    sudo apt-get install python-dev python-pip git

If you are going to use a local mysql server, additionally install 

    sudo apt-get install libmysqlclient-dev mysql-client mysql-server

This will install MySQL server, Python libraries and Git. It will ask you to set a root password [ROOT_PASSWORD] for 
the mysql server, if you haven't already set up MySQL in the past. Remember the password.

### 2. Clone the repository

    git clone https://github.com/volunteer-planner/volunteer_planner.git
    
An instance of the volunteer_planner will be created in the folder `volunteer_planner`.

### 3. Create a virtual environment

    virtualenv --no-site-packages volunteer_planner-venv
    
Enable the virtual environment by running 

bash
    
    source volunteer_planner-venv/bin/activate (for bash) or

fish . volunteer_planner-venv/bin/activate.fish

### 4. Install all requirements by running 

    cd volunteer_planner
    
For a local sqlite DB install 

    pip install -r requirements/dev.txt

or, if you intend to use mysql locally, install 

    pip install -r requirements/dev_mysql.txt

### 5. Create a local mysql database and user
    
    mysql -u root -p

    CREATE DATABASE volunteer_planner;
    GRANT ALL PRIVILEGES ON volunteer_planner.* to vp identified by 'volunteer_planner';
    \q

*Note*: For the local environment, the DB username is assumed to be 'vp' 
and their password is assumed to be 'volunteer_planner'.

### 6. Initialize the database

    ./manage.py migrate --settings=volunteer_planner.settings.local[_mysql]

### 7. Add a superuser 

    ./manlocal.py createsuperuser --settings=volunteer_planner.settings.local[_mysql]
    
You will be asked for username, email and password (twice). Remember that username and password.

### 8. Try running the server 

    ./manlocal.py runserver --settings=volunteer_planner.settings.local[_mysql]

Try opening http://localhost:8000/ in your browser.


### 9. Adding content

To add new organizations and shifts, you have to access the backend at `http://localhost:8000/admin`. 
If prompted, login with the username/password you created in step 7 (in case you don't see an error page here).

    http://localhost:8000/admin`

### 10. Importing dummy data

    ./manage.py loaddata demo_data.json  --settings=volunteer_planner.settings.local[_mysql]

## The Project

We use less for precompiling css. The less file you will find in scheduler/static/bootstrap/less/project.less

To make this work you can just initialize the folder with "npm install -g" and then let grunt watch for changes.
