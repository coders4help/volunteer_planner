# volunteer_planner
This repro hosts the code for volunteer-planner.org. A platform to schedule shifts of volunteers.

## Please do pull request against the development branch.
If you have questions concerning our workflow please look here
https://github.com/volunteer-planner/volunteer_planner/wiki/DevelopmentRules

## Setup (Ubuntu 14.04)

### 1.Install all required Ubuntu packages

    sudo apt-get install python-dev python-pip git npm

This will install Python libraries and Git.

If you are going to use a local mysql server, additionally install

    sudo apt-get install libmysqlclient-dev mysql-client mysql-server

This will install MySQL server, it will ask you to set a root password
[ROOT_PASSWORD] for the mysql server, if you haven't already set up MySQL in the
past. Remember the password.

### 2. Clone the repository

    git clone https://github.com/volunteer-planner/volunteer_planner.git

An instance of the volunteer_planner will be created in the folder
`volunteer_planner`.

### 3. Create a virtual environment using virtualenvwrapper

Create an virtualenv:
    
    $ mkvirtualenv vp

*Note*: using `vp` as your virtualenv's name is a recommendation, not a requirement. For more details on how to use virtualenvwapper, see [virtualenvwrapper docs](https://virtualenvwrapper.readthedocs.org/).

The virtual environment should be enabled afterwards. When you are working on the project,
activate the virtual env using

    $ workon vp

With your virtual env activated, install the requirements:

    $ pip install -U pip
     
    $ pip install /path/to/volunteer_planner.git/requirements/dev.txt

*Note*: `/path/to/volunteer_planner.git` means the path of your local clone of the 
GitHub project, created in step 2. Replace it accordingly with the actual path.

#### 3.1 Setup your virtualenv `postactivate` hook (optional)

Every time, an virtualenv is activated with virtualenvwrappers `workon` command, 
a `postactivate` script is executed. This comes in handy to autmatically setup 
a projects' environment variables and automate some reoccuring tasks.

A recommended `postactivate` script (found at `$VIRTUAL_ENV/bin/postactivate`)

    #!/bin/bash
    # This hook is run after this virtualenv is activated.
    ​
    export DJANGO_SETTINGS_MODULE="volunteer_planner.settings.local"
    cd /path/to/volunteer_planner.git/
    ​
    git fetch --all
    git status

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

### 6. Setup your local environment (optional)

If you need to use non-default settings values, setup the environment variables
in your virtualenv's (post-)activation hooks or your IDE's project settings.

### 7. Initialize the database

    ./manage.py migrate

### 8. Add a superuser

    ./manage.py createsuperuser

You will be asked for username, email and password (twice). Remember that
username and password.

### 9. Try running the server

    ./manage.py runserver

Try opening http://localhost:8000/ in your browser.

### 10. Adding content

To add new organizations and shifts, you have to access the backend at
`http://localhost:8000/admin`. If prompted, login with the username/password of
the superuser you created earlier (in case you don't see an error page here).

    http://localhost:8000/admin

## The Project

### Create Dummy Data

run management command " python manage.py create_dummy_data 5 --flush True " with activated virtualenv to get 5 days of dummy data and delete tables in advance.

The number (5 in the above example) creates 5 days dummy data count from today.
If you just use "python manage.py create_dummy_data 5" without --flush it is NOT deleting data before putting new data in.

### Running Tests

*Note*: we're committed to testing and hope, the next paragraph will not be a lie any longer soon :-) 

We are using test driven development (TDD) with [py.test](http://pytest.org/). 

A good read on TDD is the free o'Reilly eBook ["Test-Driven Development with Python"](http://chimera.labs.oreilly.com/books/1234000000754/index.html)

To run the tests, run the following command (with your virtual env activated, see 3.)

    $ py.test [/path/to/volunteer_planner.git/]

### Translations

Can create/update the translations file with

```
./manage.py makemessages --no-obsolete --no-wrap
```

The options are intended to make the output more git-friendly.

Compile the messages file with

```
./manage.py compilemessages
```

Your local installation should be translated then.
The .mo file created by compilemessages is gitignored,
you'll need to (re-)generate it locally every time the .po file changes.


### CSS / Less

We use less for precompiling css. The less file you will find in
`scheduler/static/bootstrap/less/project.less` To make this work you can just
initialize the folder with "npm install -g" and then let grunt watch for
changes.
