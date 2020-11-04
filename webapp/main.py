import os

from flask import Flask, Markup, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)


db.create_all()


@app.route('/')
def hello_world():
    return redirect(url_for("index"))


@app.route("/index")
def index():
    result = db.session.query(Posts).all()
    dt = []
    for res in result:
        dt.append({"username": res.username, "text": Markup(res.text)})
    return render_template("index.html", result=dt)


@app.route("/post_comment", methods=["POST"])
def post_comment():
    username = request.form["name"]
    text = request.form["comment"]
    new_comment = Posts(username=username, text=text)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/users", methods=["POST", "GET"])
def users():
    if request.method == "POST":
        username = request.form["user"]
        new_comment = Users(username=username)
        db.session.add(new_comment)
        db.session.commit()
    result = db.session.query(Users).all()
    dt = []
    for res in result:
        dt.append({"username": Markup(res.username)})
    return render_template("users.html", result=dt)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
