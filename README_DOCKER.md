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

#### 2.1 Initialize the DB container

Run `docker-compose up db`, and wait for the initialization to be over. You can now kill the container with `CTRL-c`.

#### 2.3 Initalize the web container and run migrate management command to setup non-existing tables

    $ docker-compose run --rm web migrate

#### 2.4 Add a superuser

    $ docker-compose run --rm web createsuperuser --username admin --email admin@localhost

You will be asked for password twice. Remember that password.

### 3. Run the server

    $ docker-compose up

Try opening http://localhost:8000/ in your browser. If you want to shutdown you can start the shutdown of the containers with `CTRL-c`.


## Create dummy data
If you want to create dummy data you can run:

    $ docker-compose run --rm web create_dummy_data 5 --flush True

to get 5 days of dummy data and delete tables in advance.

The number (5 in the above example) creates 5 days dummy data count from today.
If you just use `create_dummy_data 5` without `--flush True` it is NOT deleting data before putting new data in.
