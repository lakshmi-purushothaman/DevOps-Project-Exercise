# DevOps Apprenticeship: Project Exercise

## Architecture Diagram

[Architecture Diagram](https://go.gliffy.com/go/share/s284x0ldwswfqfkx7o3o)

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

The app uses TRELLO api's to store and manage the to-do items for our app, you will need to create a TRELLO account and dedicated board to store the to-do items.

To create a TRELLO account [Create Account](https://trello.com/signup), then generate API Key and Token following the [Instructions](https://trello.com/app-key)

Add the generated API Key, Token that you want to create in the .env file under the following keys:
```bash
* TRELLO_API_KEY
* TRELLO_TOKEN
```
Set Trello board name in the .env file with the following key:
```bash
* TRELLO_BOARD_NAME
```
## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## App Testing
To run the tests (Unit and Integration), use the command ``poetry run pytest todo_app_tests``. This will run any test defined in a function
matching the pattern ``test_*`` or ``*_test``, in any file matching the same patterns, in the ``todo_app_tests`` directory.

To run the selenium tests, use the command ``poetry run pytest todo_app_e2e_tests``. This will run any end to end tests defined in a function
matching the pattern ``test_*`` or ``*_test``, in any file matching the same patterns, in the ``todo_app_e2e_tests`` directory.

## Vagrant Setup
This app is setup to run on a virtual machine using Vagrant, which will setup the Todo App environment without having to worry about Python installation and it's dependecies

### Vagrant Configuration
Vagrant configuration support older styles for backwards compatibility

### Vagrant prerequisities

#### Hypervisor
Vagrant requires Hypervisor, checkout ['VirtualBox'](https://www.virtualbox.org/)

#### Vagrant
Download and install Vagrant from ['Official Website'](https://www.vagrantup.com/)

### Running Vagrant
Launch Vagrant with a command 
```bash
$ Vagrant up
```

## Docker Setup
This app is dockerized, which will setup the Todo App environment without having to worry about Python installation and it's dependecies.

There are 2 docker environments that can be run:
- Development
- Production

### To run Development docker environment
```bash
docker-compose up -d todo-app-development
```
Development environment is setup on port 5001

### To run Production docker environment
```bash
docker-compose up -d todo-app-production
```
Production environment is setup on port 5000

### Alternatively, the todo app can also be run as follows:

### To run Development environment
- cd to the directory containing Dockerfile
- Build a image
```bash
docker build --target development --tag todo-app:dev .
```
- Build a container
```bash
docker run --env-file .env -p 5001:5000 --mount type=bind,source="$(pwd)",target=/app/ todo-app:dev
```
Development environment is setup on port 5001

### To run Production environment
- cd to the directory containing Dockerfile
- Build a image
```bash
docker build --target production --tag todo-app:prod .
```
- Build a container
```bash
docker run --env-file .env -p 5000:5000 todo-app:prod
```
Production environment is setup on port 5000

### To run unit and integration tests
- cd to the directory containing Dockerfile
- Build a image
```bash
docker build --target test --tag todo-app:test .
```
- Build a container
```bash
docker run --env-file .env.test todo-app:test
```

### To run E2E Tests
- cd to the directory containing Dockerfile
- Build a image
```bash
docker build --target e2etest --tag todo-app:e2etest .
```
- Build a container
```bash
docker run --env SECRET_KEY=Your Trello Secret Key S --env MONGO_CONNECTION_STRING=Your Mongo Connection String --env DBNAME=Mongo DB Name --env COLLECTIONAME=Mongo Collection Name todo-app:e2etest
```
## Authentication and Authorisation
To avoid todo app being publicly accessible and restrict who can add new ones, GitHub Authentication using OAuth flow is used to authenticate and authorize

Please register the app using the following URL ['Github documentation'](https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app) , to create OAuth app


## CI Setup
Github actions has been setup for this repository, every push will run the build defined.

## CD Setup
Github actions continuous deployment pipeline has been setup for this repository such that, every push to main branch:
- Automatically builds and deploys to Heroku
- Pushes the images to Docker Hub

Add the following github secrets for the CD pipeline to work automatically:
- DOCKER_PASSWORD = Your Docker Password
- DOCKER_USERNAME = Your Docker Username
- HEROKU_API_KEY = Your Heroku API Key
- HEROKU_EMAIL = Your HEroku Email Address
- PORT = Heroku app listens on a port defined here
- SECRET_KEY = Secret Key
- MONGO_CONNECTION_STRING = Your Mongo Connection String
- DBNAME = Mongo DB Name
- COLLECTIONAME = Mongo Collection Name

## App Usage
App will authenticate users with github authentication using OAuth flow, currently only the admin user with writer role can perform the below actions and other users with reader role can only view the app
The App allows to:
```bash
*Add a TODO item
*Mark item as started
*Mark item as completed
*Repeat item from the completed list
*Delete item within different lists
*View the TODO list of items
```

Enter a TODO item and click on Add to add the item to TODO list