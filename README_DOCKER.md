# volunteer-planner.org Docker

An easy setup for using the Volunteer-Planner in a development or test environment is to use Docker. The Docker
configuration files are included in the git configuration of Volunteer Planner.

**Using this setup for production environments requires some further knowledge**.

This is still work-in-progress and in no way intended to be feature-complete. Suggestions are welcome, preferably by
opening an issue, describing your idea/wish/requirement.

If anyhow possible, detailed "requirement description" is more valuable to us, than pure "ready to use" solutions. We
welcome solution suggestions and are even more excited, if we can see and follow the intendment behind it.

## Project setup for development

### 1. Install docker

#### 1.1 Install docker engine

Follow [the instructions](https://docs.docker.com/engine/installation/) relevant to your operating system.

#### 1.2 Install docker-compose

Install `compose` CLI command according to
[the instruction](https://docs.docker.com/compose/cli-command/#installing-compose-v2)
relevant to your operating system.

In this readme we'll use `docker compose`. If you prefer version 1 (`docker-compose`), most probably you'll get along,
using instructions here, by substituting
`docker compose` with `docker-compose`.

### 2. Prepare the docker files

#### 2.1 Build images

Execute

```shell
docker compose build
```

This is currently necessary, because sometimes docker compose build does not reflect depedency between django image and
web image.

#### 2.1 Initialize docker network, volumes and containers

Execute

```shell
docker compose up --no-start
```

#### 2.3 Initalize by running migrations to set up non-existing tables

Execute

```shell
docker compose run -T --rm django migrate
```

#### 2.4 Add a superuser

```shell
docker compose run -T --rm django createsuperuser --username admin --email admin@localhost --no-input
docker compose run --rm changepassword admin
```

**_You will be asked for admin password twice. Remember that password._**

If you want to, feel free to change username `admin` to something you like better. Changing the e-mail address is
possible too, although it should not make a difference.

### 3. The server

To start / run the server

```shell
docker compose up
```

Try opening http://localhost:8000/ in your browser. If you want to shut down, you can initiate container shutdown
with `CTRL-c`.

URL is identical to the one of `manage.py runserver`. So please stop any possibly running `runserver` process, before
using docker.

#### 3.1 If you don't want containers block your terminal

Run

```shell
docker compose up -d
```

instead. This backgrounds containers (`detaches`), e. g. for longer period of testing UI. If you change sources, file
watch should notice it, as project directory is mounted into the running container.

#### 4. Rebuilding

Repeat steps from step 2. and 3.

To clean up everything and start from scratch:

```shell
docker compose down --volumes --remove-orphans
```

This will stop and remove any containers, connected to this `docker compose`
project, any unnamed volumes and the project docker network.

If you want or need to recreate containers because `pip` dependencies changed, you don't necessarily need to remove old
containers and volumes.

Simply

```shell
docker compose build
docker compose up --force-recreate -d
```

(or spare `-d` if you want containers in foreground), it will recreate containers, keeping anonymous volumes.

If you added a migration, you can run

```shell
docker compose run -T --rm django migrate
```

at any time - still running containers are no problem and usually don't need to be stopped or retarted

### 4. Anything else

#### 4.1 Stop all running services

To stop all eventually running servics, please execute the command

```shell
docker compose stop
```

#### 4.2 Modify configuration

Please don't ddjust the configuration in `docker-compose.yml` to reflect your desired docker changes.

Please use `docker-compose.override.yml` instead. It's untracked by git, so neither your modifications will be
accidentally committed, not will any change in repository overwrite your configuration.⌃

Those, unaware with `docker compose`: Override is meant literally. You don't have to copy everything.
Create a service entry for "about to be overriden" service(s). Set "about to be changed" values (e. g. `ports`).
Leave everything as it is, this keeps you updated with probable changes in `docker-compose.yml`.

#### 4.3 Create dummy data

If you want to create dummy data you can run:

```shell
docker compose run --rm -T django create_dummy_data 5 --flush True
```
to get 5 days of dummy data and delete tables in advance.

The number (5 in the above example) creates 5 days dummy data count from today. If you just use `create_dummy_data 5`
without `--flush True` it is NOT deleting data before putting new data in.

## Additional information

### Speeding up debugging

For better debugger performance PyCharm contains some improvements, starting in version 5.1.
See http://blog.jetbrains.com/pycharm/2016/02/faster-debugger-in-pycharm-5-1/ for more information.

To enable debugger speedups using Cython within the docker container we need some preparation.

    $ docker ps -a -f name=pycharm_helpers --format '{{.Names}}' |sort
    $ PYCHARM_VERSION=<choose from above output, matching 'About PyCharm' / 'Build'
    $ printf 'apk add --no-cache gcc musl-dev &&
        /usr/local/bin/python /opt/.pycharm_helpers/pydev/setup_cython.py build_ext --inplace' | \
         docker run --rm -i -u root --volumes-from=${PYCHARM_VERSION} --entrypoint=/bin/sh volunteer_web:latest

This needs to be repeated after PyCharm updates.
It might change, over time - please file a PR or get in contact, to get this description updated.
