from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config

from todo_app.data.session_items import get_items, add_item

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    #return 'Hello World!'
#Code that fetches all the TODO items from session
    items = get_items()
    return render_template('index.html', items=items)

@app.route('/addItem', methods=['POST','GET'])
def formHandler():
#Code that adds the TODO item added on the screen to a session
    if request.method == 'POST':
        title = request.form.get("title")
        item = add_item(title)
        return redirect(f"/")

if __name__ == '__main__':
    app.run()