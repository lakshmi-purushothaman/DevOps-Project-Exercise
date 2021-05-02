from flask import Flask, render_template, request, redirect, flash, url_for

from todo_app.flask_config import Config

from todo_app.data import session_items as session

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
#Code that fetches all the TODO items from session
    items = session.get_items()
    return render_template('index.html', items=items)

@app.route('/addItem', methods=['POST'])
def addItem():
#Code that adds the TODO item added on the screen to a session
    title = request.form.get("title")
    if title == '':
        flash('Please enter a task')
    else:
        session.add_item(title)   
    return redirect(url_for('index'))

@app.route('/markCompleted', methods=['POST'])
def markComplete():
    id = request.form.get('todo_id')
    item = session.get_item(id)
    item['status'] = "Completed"
    session.save_item(item)
    return redirect(url_for('index'))

@app.route('/deleteItem', methods=["POST"])
def deleteItem():
    id = request.form.get('todo_id')
    item = session.get_item(id)
    session.delete_item(item)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()