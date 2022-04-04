# Volunteer Planner

Volunteer Planner is a platform to schedule shifts of volunteers. Volunteers register at the platform and choose shifts.
 The admin of the website can easily add new organizations, places and shifts. The software has a location based
 hierarchy (country / region / area / city) and has a hierarchy of organizations (organizations, facilities, tasks and
  workplaces) - it can be used for a variety of purposes.

## Status
This code has been used from 2015 to 2018 and since March 2022 at volunteer-planner.org.

## Work in progress
There are some feature requests to be implemented in the future.
The software currently needs a centralized administration of the shifts, but it is one of the main goals of the current
development to empower organizations to schedule shifts for their facilities on their own.

If you are interested to contribute, join the [developer Slack channel](https://join.slack.com/t/coders4help/shared_invite/zt-1520v8cef-DytzxhO~ubmTrX0CdVcpxQ) or create a feature or fix pull request directly.

## System context
**User**: The volunteers and administrators just need a (modern) web browser to use the volunteer-planner application.

**Developer**: Developers need a python development environment (see project setup) and specific versions of external
libraries (see /requirements directory, t). Development can be done with a sqlite databases, there is no need to run
and configure postgres or mysql.

**Server**: For production use you need a Python ready web server, for example uWSGI as web server for the Python WSGI
with nginx as proxy server visible to the end user (volunteers and administrators). You also need a MySQL or PostgreSQL
database.


## Project setup for development

Note. It is also possible to get moving fast with our [Docker installation guide.](https://github.com/coders4help/volunteer_planner/blob/develop/README_DOCKER.md)

### 0. Prerequisites (Ubuntu 14.04 example)

If your machine is setup to work on Django projects, you might skip this step.

#### 0.1 Installing required OS packages

    make sys_base

This will install Python libraries and Git.

#### 0.2 Using MySQL locally (optional)

Using MySQL locally for development is optional.

#### 0.2.1 Installing MySQL (optional)

If you are going to use a local MySQL server, additionally install

    make sys_mysql

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

Please refer to the canonical [virtualenv guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for installation. We suggest you create a virtualenv named vp - so you can easily switch to your environment via

    workon vp

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

*Note:* You'll need to re-active your virtual environment after each change to it's `postactivate` hook to take effect. Just run `workon vp` again, to make sure your current venv session has executed the `postactivate` hook.

#### 2.3.1 ... settings module for using MySQL

When you prefer to use MySQL locally, you'll probably need to use the settings module `volunteer_planner.settings.local_mysql` instead of `volunteer_planner.settings.local`.

#### 2.3.2 Setup your local environment (optional)

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

Run management command

    ./manage.py create_dummy_data 5 --flush True

with activated virtualenv to get 5 days of dummy data and delete tables in advance.

The number (5 in the above example) creates 5 days dummy data count from today.
If you just use `./manage.py create_dummy_data 5` without `--flush` it is NOT deleting data before putting new data in.

### Running Tests

Feature pull requests should be accompanied by appropriate tests. We have unit and integration tests that
are run with `py.test`, and functional/behave tests that are run with `selenium`.

To run unit tests, run the following command (with your virtual env activated, see 3.)

    $ py.test -v [/path/to/volunteer_planner.git/]

If you want to generate a coverage report as well, run

    $ py.test --cov=. --cov-report html --cov-report term-missing --no-cov-on-fail -v

This generates a nice HTML coverage page, to poke around which can be found at `/path/to/volunteer_planner.git/htmlcov/index.html`.

*Note*: The directory `htmlcov` is git-ignored.

To run selenium tests, run

    $ behave tests/_behave

### Translations

We use [Transifex (tx)](https://www.transifex.com/coders4help/volunteer-planner/) for managing translations.

#### General notes

* Please read
    * [Django 1.8: Internationalization and localization](https://docs.djangoproject.com/en/1.8/topics/i18n/)
    * [Django 1.8: Translations](https://docs.djangoproject.com/en/1.8/topics/i18n/translation/)
* Please avoid internationalized strings / messages containing HTML markup. This makes the site layout depending on the translators and them getting the markup right; it's error prone and hardly maintainable when the page's layout changes.
* use `trimmed` option in [blocktrans](https://docs.djangoproject.com/en/1.8/topics/i18n/translation/#std:templatetag-blocktrans) template tags, if indention is not intended.
* Please provide [contextual markers](https://docs.djangoproject.com/en/1.8/topics/i18n/translation/#contextual-markers) on strings to help translators understanding the usage of the strings better. The shorter an internationalized string is, the more abigious it will be and the more important an contextual hint will be.

#### Workflow

1. Code your stuff using the `ugettext_lazy as _` etc. methods to mark internationalized strings
2. Update the po files `./manage.py makemessages --no-wrap --no-obsolete -l en`
   The options are intended to make the output more git-friendly.
3. Push the updated translations to git. **Do not intend to translate in the local .po files, any changes here will be overwritten when translations are pulled from [tx](https://www.transifex.com/coders4help/volunteer-planner/).**
4. Transifex will automatically update the source strings via github once a day and make them available for translation.
4.1. If necessary, translation managers (meaning VP's Transifex project admins) can update the source language manually using the tx client command `tx push -s django`.
5. Translators will then translate on [VP's Transifex project](https://www.transifex.com/coders4help/volunteer-planner/)
6. When new translations are available on Transifex `tx pull` will update the local .po files with translations from TX
7. `./manage.py makemessages --no-wrap --no-obsolete` will reformat po files in a more readable single-line message string format
8. `./manage.py compilemessages`
9. Test if it looks good and works as intended
10. Commit and push the updated translations to git

Your local installation should be translated then. The .mo file created by compilemessages is gitignored,
you'll need to (re-)generate it locally every time the .po file changes.

#### How to use the Transifex client

You first need to make sure that the transiflex client is installed (should be in the requirements/dev.txt file).

```
pip install transifex-client
```

* For further installation infos and setup read [Transifex: Client setup](http://docs.transifex.com/client/config/)
* Then, sign up at https://www.transifex.com, search for the project volunteer-planner.org, and join the respective team.
* If you used an Oauth-ish method (Google, Facebook, etc.) to sign up for Transifex, you might need to set a password in your [Transifex profile](https://www.transifex.com/user/settings/password/) before you can use the client.
* Edit your personal transifex configuration file that is stored in your home directory at ~/.transifexrc
```
[https://www.transifex.com]
username = YOUR_TRANSIFEX_USERNAME
token =
password = YOUR_TRANSIFEX_PASSWORD
hostname = https://www.transifex.com
```
Make sure not to share this file with anyone, as it contains your credentials! For more information on configuration, see http://docs.transifex.com/client/config/
