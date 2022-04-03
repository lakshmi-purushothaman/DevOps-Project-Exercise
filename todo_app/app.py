from flask import Flask, render_template, request, redirect, flash, url_for

from todo_app.data.todo import TodoService

from todo_app.ViewModel import ViewModel

from todo_app.data.todomongo import TodoMongoAccessService

import os, requests

from flask_login import LoginManager, login_required, login_user, current_user, AnonymousUserMixin
from oauthlib.oauth2 import WebApplicationClient
from functools import wraps

from todo_app.User import User, MyAnonymousUser

def create_app():
    app = Flask(__name__)
    todoMongoService = TodoMongoAccessService()

    github_oauth_client_id = os.getenv('CLIENT_ID')
    github_oauth_client_secret = os.getenv('CLIENT_SECRET')
    github_oauth_authorize_url = "https://github.com/login/oauth/authorize"
    github_oauth_token_url = "https://github.com/login/oauth/access_token"
    
    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    login_manager = LoginManager()
    login_manager.anonymous_user = MyAnonymousUser

    @login_manager.unauthorized_handler
    def unauthenticated():
        client = WebApplicationClient(github_oauth_client_id)
        return redirect(client.prepare_request_uri(github_oauth_authorize_url))

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app) 

    @app.route('/login/callback')
    def login():

        request_code = request.args.get('code')
        client = WebApplicationClient(github_oauth_client_id)
        
        token_url, headers, body = client.prepare_token_request(
            github_oauth_token_url,
            authorization_response=request.url,
            code=request_code,
            client_secret=github_oauth_client_secret
        )

        token_resp = requests.post(token_url, headers=headers, data=body)
        client.parse_request_body_response(token_resp.text)

        get_user_uri, headers, body = client.add_token('https://api.github.com/user')
        user_profile = requests.get(get_user_uri, headers=headers, data=body)
        user_profile_id=user_profile.json()["id"]
        user = User(user_profile_id)
        login_user(user)

        return redirect('/')

    def writer_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if current_user.role == "writer":
                return f(*args, **kwargs)
            else:
                flash("Permission Denied: You do not have the required role to perform this action.")
                return redirect('/')
        return wrap

    @app.route('/')
    @login_required
    def index():
    #Code that fetches all the TODO items from Trello board
        item_view_model = ViewModel(todoMongoService.get_items(), current_user.role)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/addItem', methods=['POST'])
    @login_required
    @writer_required
    def addItem():
    #Code that adds the TODO item added on the screen to a Trello board
        title = request.form.get("title")
        if title == '':
            flash('Please enter a task')
        else:
            todoMongoService.add_item(title,'Todo')   
        return redirect(url_for('index'))

    @app.route('/moveToDoing', methods=['POST'])
    @login_required
    @writer_required
    def moveToDoing():
    #Code that marks the Todo item as Doing in Trello board
        id = request.form.get('todo_id')
        todoMongoService.update_todo_item_status(id,'Doing')
        return redirect(url_for('index'))

    @app.route('/moveToDone', methods=['POST'])
    @login_required
    @writer_required
    def moveToDone():
    #Code that marks the TODO item as DONE in Trello board
        id = request.form.get('todo_id')
        todoMongoService.update_todo_item_status(id,'Done')
        return redirect(url_for('index'))

    @app.route('/moveToTodo', methods=['POST'])
    @login_required
    @writer_required
    def moveToTodo():
    #Code that marks the DONE item as TODO in Trello board
        id = request.form.get('todo_id')
        todoMongoService.update_todo_item_status(id,'Todo')
        return redirect(url_for('index'))

    @app.route('/deleteItem', methods=["POST"])
    @login_required
    @writer_required
    def deleteItem():
    #Code that deletes the TODO item in Trello board
        id = request.form.get('todo_id')
        todoMongoService.delete_item(id)
        return redirect(url_for('index'))

    return app