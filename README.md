# volunteer_planner

A platform to schedule shifts of volunteers. 

## Project Setup

### 0. Prerequisites (Ubuntu 14.04 example) 

If your machine is setup to work on Django projects, you might skip this step.

#### 0.1 Installing required OS packages

    sudo apt-get install python-dev python-pip git npm

This will install Python libraries and Git.

#### 0.2 Using MySQL locally (optional)

Using MySQL locally for development is optional.

#### 0.2.1 Installing MySQL (optional) 

If you are going to use a local MySQL server, additionally install

    sudo apt-get install libmysqlclient-dev mysql-client mysql-server

This will install MySQL server, it will ask you to set a root password
[ROOT_PASSWORD] for the MySQL server, if you haven't already set up MySQL in the
past. Remember the password.

#### 0.2.2 Creating a local MySQL database and user (optional)

Open the MySQL shell
 
    mysql -u root -p

and execute following queries to setup the DB 

    CREATE DATABASE volunteer_planner;
    GRANT ALL PRIVILEGES ON volunteer_planner.* to vp identified by 'volunteer_planner';

*Note*: For the local environment, the DB username is assumed to be 'vp'
and their password is assumed to be 'volunteer_planner'.

### 1. Fork us on GitHub

Please fork us on GitHub and clone your fork

    git clone https://github.com/YOUR_GITHUB_ACCOUNT/volunteer_planner.git

### 1.1 Creating Pull Requests

Please do Pull Requests against the [`develop` branch](https://github.com/volunteer-planner/volunteer_planner/tree/develop).

If you have questions concerning our workflow please read the 
[Development Rules wiki page](https://github.com/volunteer-planner/volunteer_planner/wiki/DevelopmentRules).

### 2. Setup your virtual environment

#### 2.1. Create a virtual env

Create an virtualenv (using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/)):
    
    $ mkvirtualenv vp

*Note*: using `vp` as your virtualenv's name is a recommendation, not a requirement.

The virtual environment should be enabled afterwards. 
For starting/continuing working on the project using the virtualenv, 
activate the virtual env using

    $ workon vp

#### 2.2 Installing required python packages

Update pip
 
    pip install -U pip

For a local sqlite DB install

    pip install -r /path/to/volunteer_planner.git/requirements/dev.txt

or, if you intend to use MySQL locally, install

    pip install -r /path/to/volunteer_planner.git/requirements/dev_mysql.txt

*Note*: `/path/to/volunteer_planner.git` means the path of your local clone of the 
GitHub project. Replace it accordingly with the actual path.

#### 2.3 Setup your virtualenv `postactivate` hook (optional)

This step is optional but recommended. 

Every time, a virtualenv is activated with virtualenvwrappers' `workon` command, 
a `postactivate` script is executed. This comes in handy to autmatically setup 
a projects' environment variables and automate some reoccuring tasks. 
For more details on virtualenvwrapper hooks, see [virtualenvwrapper: Per-User Customization](http://virtualenvwrapper.readthedocs.org/en/latest/scripts.html). 

You might consider to use this example `postactivate` script 
(located at `$VIRTUAL_ENV/bin/postactivate`)

    #!/bin/bash
    # This hook is run after this virtualenv is activated.
    ​
    export DJANGO_SETTINGS_MODULE="volunteer_planner.settings.local"
    cd /path/to/volunteer_planner.git/
    ​
    git fetch --all
    git status

#### 2.3.1 Setup your local environment (optional)

Also, if you need to use non-default settings values, setting (exporting) the 
environment variables in your virtualenvs' `postactivate` hook is a good place 
if you're not using an IDE to configure your environment variables. 


### 3. Initialize the database with Django

Activate your env and change dir to your local forks' git repository (if not done yet).
 
    workon vp
    cd /path/to/volunteer_planner.git

#### 3.1 Run migrate management command to setup non-existing tables 
    
    ./manage.py migrate

### 3.2 Add a superuser
    
    ./manage.py createsuperuser

You will be asked for username, email and password (twice). Remember that
username and password.

### 4. Try running the server

    ./manage.py runserver

Try opening http://localhost:8000/ in your browser.

### 5. Adding content

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

    $ py.test -v [/path/to/volunteer_planner.git/]

If you want to generate a coverage report as well, run

    $ py.test --cov=. --cov-report html --cov-report term-missing --no-cov-on-fail -v

This generates a nice HTML coverage page, to poke around which can be found at `/path/to/volunteer_planner.git/htmlcov/index.html`. 

*Note*: The directory `htmlcov` is git-ignored.

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
