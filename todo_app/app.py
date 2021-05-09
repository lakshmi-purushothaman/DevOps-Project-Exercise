from flask import Flask, render_template, request, redirect, flash, url_for

from todo_app.flask_config import Config

from todo_app.data import session_items as session

from todo_app.data import todo as todo

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
#Code that fetches all the TODO items from Trello board
    items = todo.get_items()
    return render_template('index.html', items=items)

@app.route('/addItem', methods=['POST'])
def addItem():
#Code that adds the TODO item added on the screen to a Trello board
    title = request.form.get("title")
    if title == '':
        flash('Please enter a task')
    else:
        todo.add_item(title)   
    return redirect(url_for('index'))

@app.route('/markCompleted', methods=['POST'])
def markComplete():
#Code that marks the TODO item as DONE in Trello board
    id = request.form.get('todo_id')
    todo.complete_item(id)
    return redirect(url_for('index'))

@app.route('/deleteItem', methods=["POST"])
def deleteItem():
#Code that deletes the TODO item in Trello board
    id = request.form.get('todo_id')
    todo.delete_item(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()