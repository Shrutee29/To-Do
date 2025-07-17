from flask import Flask, render_template, request, redirect 
import re
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title =db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(400),nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} - {self.date_created.strftime('%Y-%m-%d%H:%M%S')}"
    
    
@app.route('/',methods = ['GET','POST'])
def hello_world():
    if request.method=='POST':
        # print("POST request received")
        title=request.form['title']
        desc=request.form['desc']
        # print(title)
        # print(desc)
        
        
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    print(alltodo) 
    return render_template('index.html',alltodo=alltodo)
    # return 'Hello, World!'

@app.route('/show')
def products():
    alltodo = Todo.query.all()
    print(alltodo)
    return 'This is product page'

@app.route('/delete/<int:sno>')
def delete(sno):
    alltodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>',methods = ['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
   

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port=int(os.environ.get('PORT',5000))    
    app.run(debug=False,host='0.0.0.0',port=port)