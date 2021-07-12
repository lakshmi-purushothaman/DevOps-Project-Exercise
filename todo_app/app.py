from flask import Flask, render_template, request, redirect, flash, url_for

from todo_app.flask_config import Config

from todo_app.data.todo import TodoService

from todo_app.ViewModel import ViewModel

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())  
    
    todoService = TodoService()

    @app.route('/')
    def index():
    #Code that fetches all the TODO items from Trello board
        item_view_model = ViewModel(todoService.get_items())

        return render_template('index.html', view_model=item_view_model)

    @app.route('/addItem', methods=['POST'])
    def addItem():
    #Code that adds the TODO item added on the screen to a Trello board
        title = request.form.get("title")
        if title == '':
            flash('Please enter a task')
        else:
            todoService.add_item(title)   
        return redirect(url_for('index'))

    @app.route('/moveToDoing', methods=['POST'])
    def moveToDoing():
    #Code that marks the Todo item as Doing in Trello board
        id = request.form.get('todo_id')
        todoService.move_to_doing(id)
        return redirect(url_for('index'))

    @app.route('/moveToDone', methods=['POST'])
    def moveToDone():
    #Code that marks the TODO item as DONE in Trello board
        id = request.form.get('todo_id')
        todoService.move_to_done(id)
        return redirect(url_for('index'))

    @app.route('/moveToTodo', methods=['POST'])
    def moveToTodo():
    #Code that marks the DONE item as TODO in Trello board
        id = request.form.get('todo_id')
        todoService.move_to_todo(id)
        return redirect(url_for('index'))

    @app.route('/deleteItem', methods=["POST"])
    def deleteItem():
    #Code that deletes the TODO item in Trello board
        id = request.form.get('todo_id')
        todoService.delete_item(id)
        return redirect(url_for('index'))

    return app