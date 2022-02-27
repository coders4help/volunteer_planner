# volunteer-planner.org Docker
An easy setup for using the Volunteer-Planner in a development or test environment is to user Docker.
The Docker configuration files are included in the git package of volunteer-planner.

**Do not use this setup for production environments**.
The web container is not secure. If you want to use docker for production you have to exchange the webserver in the web
container.

## Project setup for development

### 1. Install docker

Follow [the instructions](https://docs.docker.com/engine/installation/) relevant to your operating system.

### 2. Prepare the docker files

#### 2.1 Prepare the DB

By default, the application will be using MySQL. If you prefer PostgreSQL, edit
the `Dockerfile` and `docker-compose.yml` files, uncommenting the PostgreSQL
related parts, and commenting out the MySQL related ones.

#### 2.1 Initialize docker network, volumes and the DB container

Execute `docker-compose up --no-start db`.

#### 2.3 Initalize the web container and run migrate management command to setup non-existing tables

    $ docker-compose run --rm django migrate

#### 2.4 Add a superuser

    $ docker-compose run --entrypoint=python --rm django manage.py createsuperuser --username admin --email admin@localhost

You will be asked for password twice. Remember that password.
(Sorry for the lengthy command line, but our work to make the Django app shut down properly removes it's TTY access when using the default entrypoint.)

### 3. Run the server

    $ docker-compose up

Try opening http://localhost:8000/ in your browser. If you want to shutdown you can start the shutdown of the containers with `CTRL-c`.

### 4. Switch database

#### 4.1 Stop all running services

To stop all eventually running servics, please execute the command

    $ docker-compose stop

#### 4.2 Modify configuration

Adjust the configuration in ```docker-compose.yml``` to reflect your desired
database type. Look for all "MySQL" or "PostgreSQL" comments to find all locations you need to switch.

#### 4.3 Recreate containers

To switch the database one needs to recreate used containers.
The DB container needs to be started from a different image, using different configuration and volume.
The Web container needs to use different Django settings, while startup.

One has to forcibly remove the current containers and create new ones.
The final step is to update-initialize the database.

    $ docker-compose rm -a -v -f
    $ docker-compose create --force-recreate
    $ docker-compose start db
    $ docker-compose run --rm django migrate

If you haven't created the superuser in the new database environment, you need to execute the command from above to create it.

## Create dummy data
If you want to create dummy data you can run:

    $ docker-compose run --rm django create_dummy_data 5 --flush True

to get 5 days of dummy data and delete tables in advance.

The number (5 in the above example) creates 5 days dummy data count from today.
If you just use `create_dummy_data 5` without `--flush True` it is NOT deleting data before putting new data in.

## Additional information

### Running with docker container from within PyCharm (2016)

- Make sure, docker plugin is installed and activated
  - Preferences / Plugins / Docker integration
- Configure docker
  - Preferences / Build, Execution, Deployments / Docker
  - Create new configuration using ```+``` (or modify existing)
  - Choose a reasonable name
  - Add (or modify) ```API URL```
    - see ```docker-machine env``` and it's ```DOCKER_HOST``` value, replace ```tcp://``` with ```http://```
  - Add (or modify) ```Certificated folder```
    - see ```DOCKER_CERT_PATH```
  - Fill ```Docker Compose executable```
  - Check ```Import credentials from Docker Machine```
  - Fill ```Docker Machine executable```
  - Use ```Detect```
  - Choose ```Machine```
- Set up remote python interpreter
  - Preferences / Project: ... / Project Interpreter
  - Create ```Project Interpreter``` by using ```[...]``` and choose ```Àdd Remote```
    - ```Configure Remote Python Interpreter``` by choosing ```Docker```
    - Choose ```Server```
    - Use ```volunteer_web:latest``` as ```Image name```
    - Use ```/usr/local/bin/python``` as ```Python interpreter path```
- Create run configuration
  - Open run configurations, by choosing ```Edit Configurations...```
  - Create new ```Python``` run configuration
  - Choose a reasonable name
  - Choose ```manage.py``` within project as Script
  - Use ```runserver 0.0.0.0:8000``` as Script parameter
  - Configure ```Environment variables```
    - ```PYTHONUNBUFFERED=1```
    - ```DJANGO_SETTINGS_MODULE=volunteer_planner.settings.docker_mysql``` (if using PostgreSQL modify appropriately)
  - Choose created remote python interpreter as ```Python interpreter```
  - Set project directory as ```Working directory```
  - Set ```Path mappings```
    - ```<project directory>=/opt/vpcode```
  - Check ```Add content roots to PYTHONPATH```
  - Uncheck ```Add source roots to PYTHONPATH```
  - Configure ```Docker container settings```
    - ```Network mode```: volunteer_default
    - ```Container port```: ```8000/tcp``` = ```0.0.0.0:8000```
    - ```Link name```: ```volunteer_db_1``` aliased to ```db```
    - ```Volume bindings```: ```Container path /opt/vpcode``` = ```Host path <project path>```
    - ```Environment variables```: ```DJANGO_SETTINGS_MODULE=volunteer_planner.settings.docker_mysql``` (or ```_postgres```)
- Eventually add IP address used by ```pydevd``` to connect to PyCharm as alias
  - IP seems to be 'more or less fixed'
  - ```sudo ifconfig lo0 alias 10.0.2.2```
  - ```pydevd``` can now connect from within docker container to PyCharm listener

### Speeding up debugging

For better debugger performance PyCharm contains some improvements, starting in version 5.1.
See http://blog.jetbrains.com/pycharm/2016/02/faster-debugger-in-pycharm-5-1/ for more information.

To enable debugger speedups using Cython within the docker container we need some preparation.

    $ docker ps -a -f name=pycharm_helpers --format '{{.Names}}' |sort
    $ PYCHARM_VERSION=<choose from above output, matching 'About PyCharm' / 'Build'
    $ printf 'apk add --no-cache gcc musl-dev &&
        /usr/local/bin/python /opt/.pycharm_helpers/pydev/setup_cython.py build_ext --inplace' | \
         docker run --rm -i -u root --volumes-from=${PYCHARM_VERSION} --entrypoint=/bin/sh volunteer_web:latest

This needs to be repeated after PyCharm updates
