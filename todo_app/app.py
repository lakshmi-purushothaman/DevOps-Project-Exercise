from flask import Flask, render_template, request, redirect, flash, url_for

from todo_app.flask_config import Config

from todo_app.data.todo import TodoService

app = Flask(__name__)
app.config.from_object(Config)

todoService = TodoService()

@app.route('/')
def index():
#Code that fetches all the TODO items from Trello board
    items = todoService.get_items()
    return render_template('index.html', items=items)

@app.route('/addItem', methods=['POST'])
def addItem():
#Code that adds the TODO item added on the screen to a Trello board
    title = request.form.get("title")
    if title == '':
        flash('Please enter a task')
    else:
        todoService.add_item(title)   
    return redirect(url_for('index'))

@app.route('/markCompleted', methods=['POST'])
def markComplete():
#Code that marks the TODO item as DONE in Trello board
    id = request.form.get('todo_id')
    todoService.complete_item(id)
    return redirect(url_for('index'))

@app.route('/deleteItem', methods=["POST"])
def deleteItem():
#Code that deletes the TODO item in Trello board
    id = request.form.get('todo_id')
    todoService.delete_item(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()