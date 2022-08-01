from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import PrimaryKeyConstraint, desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///notes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Notes(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(2000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/", methods=['GET', 'POST'])
def home_pg():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        notes = Notes(title=title, desc=desc)
        db.session.add(notes)
        db.session.commit()
    allNotes = Notes.query.all()
    return render_template('home.html', allNotes = allNotes)

@app.route("/index", methods=['GET', 'POST'])
def new_nt():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        notes = Notes(title=title, desc=desc)
        db.session.add(notes)
        db.session.commit()
    allNotes = Notes.query.all()
    return render_template('index.html', allNotes = allNotes)

@app.route("/open/<int:sno>")
def open_nt(sno):
    notes = Notes.query.filter_by(sno=sno).first()
    return render_template('open.html', notes = notes)

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update_nt(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        notes = Notes.query.filter_by(sno=sno).first()
        notes.title = title
        notes.desc = desc
        db.session.add(notes)
        db.session.commit()
        return redirect("/")

    notes = Notes.query.filter_by(sno=sno).first()
    return render_template('update.html', notes = notes)

@app.route("/delete/<int:sno>")
def delete_nt(sno):
    notes = Notes.query.filter_by(sno=sno).first()
    db.session.delete(notes)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)