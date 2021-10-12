from flask import Flask, json, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    important = db.Column(db.Integer, default=0)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id', ondelete="CASCADE"))

    def __repr__(self):
        return f"Todo('{self.id}', '{self.content}', '{self.list_id}')"


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('Todo', backref='list', cascade="all, delete", lazy='dynamic')

    def __repr__(self):
        return f"List('{self.id}', '{self.name}', '{self.tasks}')"

####################################


@app.route('/', methods=['POST', 'GET'])
def create_list():
    if request.method == 'POST' and 'list' in request.form:
        lista = request.form['list']
        new_list = List(name=lista)

        try:
            if 0 < len(lista) < 50:
                db.session.add(new_list)
                db.session.commit()
                list = List.query.filter_by(name=lista).first()
                id = list.id
                return redirect(f'/{id}')
            else:
                return 'List name is too long'
        except:
            return 'There was an error while adding the task'

    else:
        lists = List.query.all()
        return render_template('index.html', lists=lists)


@app.route('/<int:id>', methods=['POST', 'GET'])
def create_task(id):
    if request.method == 'POST' and 'submit_task' in request.form:
        task_content = request.form['content']
        li = List.query.filter_by(id=id).first()
        lis = List.query.get(li.id)
        new_task = Todo(content=task_content, list=lis)

        try:
            if 0 < len(task_content) < 300:
                db.session.add(new_task)
                db.session.commit()
                return display_task(id)
            else:
                return 'Task name is too long'

        except:
            return 'There was an error while adding the task'

    else:
        return display_task(id)


def display_task(id):
    list = List.query.filter_by(id=id).first()
    li = List.query.get(list.id)

    taski = Todo.query.filter_by(list=li).order_by('data_created')
    lists = List.query.all()
    id=id
    type_of_task = li.name
    task_remaining = Todo.query.filter_by(list=li).all()

    return render_template('index.html', lists=lists, taski=taski, id=id, type_of_task=type_of_task, task_remaining=task_remaining)


@app.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    if request.method == 'POST':

        try:
            global task
            tasks_to_delete = request.form['delete'].split(',')

            for i in tasks_to_delete:
                task = Todo.query.get(i)
                db.session.delete(task)
                db.session.commit()

            # return display_task(id)
            return redirect(f'/{id}')
        except:
            return 'There was an error while deleting that task'


@app.route('/<int:id>/clear_list', methods=['GET'])
def clear(id):
    if request.method == 'GET':
        try:
            list = List.query.filter_by(id=id).first()
            li = List.query.get(list.id)
            Todo.query.filter_by(list=li).delete()
            db.session.commit()
            return redirect(f'/{id}')
        except:
            return 'There was an error while clearing list'


@app.route('/<int:id>/delete_list', methods=['GET'])
def delete_list(id):
    if request.method == 'GET':
        try:
            list = List.query.get_or_404(id)
            db.session.delete(list)
            db.session.commit()

            return redirect('/')
        except:
            return 'There was an error while deleting list'

##########################################
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('update.html', task=task)


@app.route('/important/<int:id>', methods=['GET'])
def important(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'GET':
        try:
            if task.important == 0:
                task.important = 1
                task.content = task.content.upper()
            else:
                task.important = 0
                task.content = task.content.lower()
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        return redirect('/update/9')