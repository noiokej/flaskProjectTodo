from flask import Flask, render_template, request, redirect, url_for
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
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

    def __repr__(self):
        return f"Todo('{self.id}', '{self.content}', '{self.list_id}')"


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    tasks = db.relationship('Todo', backref='list', lazy='dynamic')

    def __repr__(self):
        return f"List('{self.id}', '{self.name}', '{self.tasks}')"

####################################

@app.route('/', methods=['POST', 'GET'])
# def hom():
#     lists=List.query.all()
#     return render_template('index.html', lists=lists)
#     # return 'ffff'


def create_list():
    if request.method == 'POST':
        lista = request.form['list']
        new_list = List(name=lista)

        try:
            db.session.add(new_list)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while adding the task'

    else:
        tasks = Todo.query.all()
        lists = List.query.all()
        # return render_template("index.html", tasks=tasks, lists=lists)
        # return 'xddd'
        lists = List.query.all()
        return render_template('index.html', lists=lists)


@app.route('/<int:id>', methods=['POST', 'GET'])
def create_task(id):
    if request.method == 'POST' and 'submit_task' in request.form:
        task_content = request.form['content']
        # nazwa = request.form['nazwa']
        # li = List.query.filter_by(name=nazwa).first()
        li = List.query.filter_by(id=id).first()
        lis = List.query.get(li.id)
        new_task = Todo(content=task_content, list=lis)

        try:
            db.session.add(new_task)
            db.session.commit()
            return display_task(id)

        except:
            return 'There was an error while adding the task'

    else:
        return display_task(id)
        # tasks = Todo.query.all()
        # lists = List.query.all()
        # return render_template("index.html", tasks=tasks, lists=lists)


def display_task(id):
    list = List.query.filter_by(id=id).first()
    li=List.query.get(list.id)

    taski = Todo.query.filter_by(list=li).order_by('data_created')
    lists = List.query.all()
    id=id
    type_of_task = li.name
    task_remaining = Todo.query.filter_by(list=li).all()

    return render_template('index.html', lists=lists, taski=taski, id=id, type_of_task=type_of_task, task_remaining=task_remaining)



##########################################
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while deleting that task'


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