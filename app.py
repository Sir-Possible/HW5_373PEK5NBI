from flask import Flask, render_template, request, redirect
import json, os 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
db = SQLAlchemy(app)


migrate = Migrate(app, db)


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(50), nullable=False)
    Budget = db.Column(db.String(50), nullable=False)
    Year = db.Column(db.String(50), nullable=False)
    Cast = db.Column(db.String(50), nullable=False)
    director = db.Column(db.String(50), nullable=True)


@app.route("/")
def index():
    db = Movies.query.all()
    return render_template("index.html", movies=db)


@app.route("/new-movie", methods=['POST', 'GET'])
def new_movie():

    if request.method == 'GET':
        return render_template("new_movie.html")
    else:

        m = Movies()
        m.Title = request.form['Title']
        m.Budget = request.form['Budget']
        m.Cast = request.form['Cast']
        m.Year = request.form['Year']


        db.session.add(m)
        db.session.commit()

        return render_template(
            "new_movie.html",
            success = f"Movie '{m.Title}' was successfully added."
        )


@app.route("/edit/<string:Title>", methods=['POST', 'GET'])
def edit_movie(Title):

    m = Movies.query.filter_by(Title=Title).first()
    if request.method == 'GET':
        return render_template("edit.html", movie=m)

    else:
        m.Title = request.form['Title']
        m.Year = request.form['Year']
        m.Budget = request.form['Budget']
        m.Cast = request.form['Cast']
        
        db.session.commit()
        return render_template("edit.html", movie=m, msg=f"{m.Title} successfully updated")

@app.route("/search")
def search():
    q = request.args.get("q")
    results = Movies.query.filter(Movies.Title.contains(q)).all()
    return render_template("search.html", results = results, q=q)

@app.route("/delete/<int:id>", methods=['POST','GET'])
def delete(id):
    m = Movies.query.get(id)

    if m is None:
        return render_template("error.html")

    if request.method == 'GET':
        return render_template("delete.html", movie=m)
    else:
        db.session.delete(m)
        db.session.commit()
        return redirect("/")





















# @app.route("/")
# def index():
#     movies = {}

#     if os.path.exists("movies.json"):

#         with open("movies.json") as movies_file:
#             movies = json.load(movies_file)

#     else:
#         with open("movies.json", "w") as f:
#              f.write("[]")

#         new_movie = [{
#             "Title": "Prison-Break",
#             "Year": 2005,
#             "Budget": "USD 700m",
#             "Cast": "People" 
#         }]
#         movies = new_movie

#     return render_template("index.html", movies = movies)

# @app.route("/new-movie", methods=['POST','GET'])
# def new_movie():

#     if request.method == 'GET':
#         return render_template("new_movie.html")

#     else:
#         new_movie = {}
#         new_movie['Title'] = request.form['Title']
#         new_movie['Year']= request.form['Year']
#         new_movie['Budget'] = request.form['Budget']
#         new_movie['Cast'] = request.form['Cast']

#         with open("movies.json", "w") as f:
#             json.dump(new_movie,f)

#         return render_template("new_movie.html", success = f"Movie '{new_movie['Title']}' was successfully added.")


