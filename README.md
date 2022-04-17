# Volunteer Planner

Volunteer Planner is a platform to schedule shifts of volunteers. Volunteers register at the platform and choose shifts.
 The admin of the website can easily add new organizations, places and shifts. The software has a location based
 hierarchy (country / region / area / city) and has a hierarchy of organizations (organizations, facilities, tasks and
  workplaces) - it can be used for a variety of purposes.

## Status
This code has been used from 2015 to 2018 and since March 2022 at volunteer-planner.org.

## Work in progress
There are some feature requests to be implemented in the future.

If you are interested to contribute, you're invited to send an 
[email](mailto:kontakt@volunteer-planner.org?subject=Slack%20Invitation%20Request) 
to join the developer Slack channel or create a feature or fix pull request directly.

## System context
**User**: The volunteers and administrators just need a (modern) web browser to use the volunteer-planner application.

**Developer**: Developers need a python development environment (see project setup) and specific versions of external
libraries (see ./requirements directory). Development can be done with a sqlite databases, there is no need to run
and configure postgres - although it's nevertheless a good idea.
If you develop using sqlite you can test postgres compatibility by using docker: a `Dockerfile` and a `docker-compose.yml` 
file are provided.

**Server**: For production use you need a Python ready web server, for example uWSGI as web server for the Python WSGI
with nginx as proxy server visible to the end user (volunteers and administrators). You also need a PostgreSQL database.

## Project setup for development

Note. It is also possible to get moving fast with our [Docker installation guide.](https://github.com/coders4help/volunteer_planner/blob/develop/README_DOCKER.md)

### 0. Prerequisites

If you already have a local setup to work in Django projects, you're (almost) done.
If you want to develop using sqlilte, you actually are.
If you prefer to develop against productively used postgres, you most probably need to set up a database.

If you're done, skip to [Step 1](#step_01)

#### 0.1 Required software 

### 0. Prerequisites

If your machine is set up to work on Django projects, you might skip this step.
Otherwise, the most basic required software is

- python
- pip
- virtualenv (any variant)
- git

#### 0.1 Installing required OS packages

Use software management of your choise, whether `apt`, `yum`, `brew` or any other.

Search for `python`, `pip` and `git`.

#### 0.2 Using PostgreSQL locally (optional)

Using PostgreSQL locally for development is optional.

#### 0.2.1 Installing PostgreSQL (optional)

If you are going to use a local PostgreSQL server, additionally make sure, it's installed and test it's running.

#### 0.2.2 Creating a local PostgreSQL database and user (optional)

Open the PostgreSQL shell, by using `psql`, as superuser (usually `postgres` but that depends on your installation)
and execute following queries to set up the DB

    CREATE USER vp WITH LOGIN PASSWORD 'volunteer_planner';
    ALTER USER vp PASSWORD 'volunteer_planner';
    CREATE DATABASE volunteer_planner OWNER vp;

*Note*: For the local environment, the database username is assumed to be `vp`
and their password is assumed to be `volunteer_planner`.

### <a name="step_01">1. Fork us on GitHub</a>

Please [fork us on GitHub](https://github.com/coders4help/volunteer_planner/fork) and 
clone your fork

    git clone https://github.com/YOUR_GITHUB_ACCOUNT/volunteer_planner.git

### 1.1 Creating Pull Requests

Please do Pull Requests against the [`develop` branch](https://github.com/volunteer-planner/volunteer_planner/tree/develop).

If you have questions concerning our workflow please read the
[Development Rules wiki page](https://github.com/volunteer-planner/volunteer_planner/wiki/DevelopmentRules).

### 2. Setup your virtual environment

#### 2.1. Create and activate a virtual env

Please refer to the canonical [virtualenv guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for installation. 

The most basic way is, to create a virtualenv in your project directory:

    cd /path/to/volunteer_planner.git/
    virtualenv .venv
    . ./.venv/bin/activate

`.venv` will be excluded from `git` interactions, and you will know where the virtualenv is located, so you can clean up, 
if something is too broken.  

If you preferred to use `virtualenvwrapper`, you'd do:

    mkvirtualenv vp
    workon vp

python-guide's first choise is `pipenv` and it's usage is simple as well:

    cd /path/to/volunteer_planner.git/
    pipenv shell

#### 2.2 Installing required python packages

All the following steps assume, your shell' / execution environment's current working directory is the project directory.

Optionally update pip

    pip install -U pip

For a local sqlite DB install

    pip install -r requirements/dev.txt

or, if you intend to use PostgreSQL locally, install

    pip install -r requirements/dev_postgres.txt

#### 2.3 Setup your virtualenv `postactivate` hook (optional)

This step is optional but recommended.

Every time, a virtualenv is activated with virtualenvwrappers' `workon` command,
a `postactivate` script is executed. This comes in handy to autmatically set up
a projects' environment variables and automate some reoccuring tasks.
For more details on virtualenvwrapper hooks, see [virtualenvwrapper: Per-User Customization](http://virtualenvwrapper.readthedocs.org/en/latest/scripts.html).

You might consider using this example `postactivate` script
(located at `$VIRTUAL_ENV/bin/postactivate`)

    #!/bin/bash
    # This hook is run after this virtualenv is activated.
    ​
    export DJANGO_SETTINGS_MODULE="volunteer_planner.settings.local"
    cd /path/to/volunteer_planner.git/
    ​
    git fetch --all
    git status

*Note:* You'll need to re-active your virtual environment after each change to it's `postactivate` hook to take effect. 
Just run `workon vp` again, to make sure your current venv session has executed the `postactivate` hook.

#### 2.3.1 ... settings module for using PostgreSQL

When you prefer to use PostgreSQL locally, you'll probably need to use the settings module 
`volunteer_planner.settings.local_postgres` instead of `volunteer_planner.settings.local`.

#### 2.3.2 Setup your local environment (optional)

Also, if you need to use non-default settings values, setting (exporting) the
environment variables in your virtualenvs' `postactivate` hook is a good place
if you're not using an IDE to configure your environment variables.

If you're using `pipenv`, having your environment variable settings in a `.env` file in your project directory will be
sufficient. `pipenv shell` will load this file.

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
    * [Django 4.0: Internationalization and localization](https://docs.djangoproject.com/en/4.0/topics/i18n/)
    * [Django 4.0: Translations](https://docs.djangoproject.com/en/4.0/topics/i18n/translation/)
* Please avoid internationalized strings / messages containing HTML markup. This makes the site layout depending on the 
  translators and them getting the markup right; it's error-prone and hardly maintainable when the page's layout changes.
* use `trimmed` option in [blocktrans](https://docs.djangoproject.com/en/4.0/topics/i18n/translation/#std:templatetag-blocktrans) 
  template tags, if indention is not intended.
* Please provide [contextual markers](https://docs.djangoproject.com/en/4.0/topics/i18n/translation/#contextual-markers) 
  on strings to help translators understanding the usage of the strings better. The shorter an internationalized string 
  is, the more abigious it will be and the more important an contextual hint will be.

#### Workflow

1. Code your stuff using the `gettext_lazy as _` etc. methods to mark internationalized strings
2. Update the po files `./scripts/makemessages.sh -l en`
   The scripts and its options are intended to make the output more git-friendly.
3. Push the updated translations to git. **Do not intend to translate in the local .po files, any changes here will be 
   overwritten when translations are pulled from [tx](https://www.transifex.com/coders4help/volunteer-planner/).**
4. Used to be: Transifex will automatically update the source strings via github once a day and make them available for translation.
4.1. If necessary, translation managers (meaning VP's Transifex project admins) can update the source language manually 
     using the tx client command `tx push -s django`.
5. Translators will then translate on [VP's Transifex project](https://www.transifex.com/coders4help/volunteer-planner/)
6. When new translations are available on Transifex `tx pull` will update the local .po files with translations from TX
7. `./checkmessages.sh` will reformat po files in a more readable single-line message string format and compile mo files
8. Test if it looks good and works as intended
9. Commit and push the updated translations to git

Your local installation should be translated then. The .mo file created by compilemessages is gitignored,
you'll need to (re-)generate it locally every time the .po file changes.

#### How to use the Transifex client

We're about to transit to the current transifex client, because the one used at the moment is deprecated.
It uses old API, which will be deactivated end of 2022.
Until we're finished with transition, the following guide still works.

You first need to make sure that the transiflex client is installed (should be in the requirements/dev.txt file).

```
pip install transifex-client
```

* For further installation infos and setup read [Transifex: Client setup](http://docs.transifex.com/client/config/)
* Then, sign up at https://www.transifex.com, search for the project volunteer-planner.org, and join the respective team.
* If you used an Oauth-ish method (Google, Facebook, etc.) to sign up for Transifex, you might need to set a password in 
  your [Transifex profile](https://www.transifex.com/user/settings/password/) before you can use the client.

