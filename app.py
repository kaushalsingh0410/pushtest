from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    description = db.Column(db.String(500),nullable = False)
    created_at = db.Column(db.DateTime,default = db.func.now())

    def __repr__(self):
        return f"{self.sno} {self.title}"

with app.app_context():
    db.create_all()




@app.route('/Ritu')
def Ritu():
    return 'Ritu this is Flask Todo App'

@app.route('/',methods = ['POST','GET'])
def index():
    # return 'Hi ritu'
    if request.method == 'POST':
        print('Ritu inside if')
        print('Title',request.form['title'],'Description',request.form['description'])
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title =title ,description = description)
        db.session.add(todo)
        db.session.commit()
    todos = Todo.query.order_by(desc(Todo.sno)).all()
    return render_template('index.html',todos = todos)


@app.route('/detete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:sno>',methods = ['POST','GET'])
def update(sno):
    
    if request.method == 'POST':
        todo = Todo.query.filter_by(sno = sno).first()
        print()
        todo.title = request.form['title'] 
        todo.description = request.form['description']
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno = sno).first()
    print('HI ritu',todo.title)
    return render_template('update.html',todo = todo)


if __name__ == '__main__':
    app.run(debug = True,port = 8000)