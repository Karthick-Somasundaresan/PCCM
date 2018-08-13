from flask import Flask, render_template, request
import trials.MovieAnalyser as MovieAnalyser


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello Flask"


@app.route('/home')
def home():
    movies = [{"poster": "./static/Pirates1.jpg", "name":" Pirates 1", "id": "asset1"},
              {"poster": "./static/Pirates1.jpg", "name": " Pirates 2", "id": "asset2"}]
    return render_template('HomePage.html', movies=movies)


@app.route('/surveyMovie')
def surveyMovie():
    movie_id = request.args.get('id')
    words = MovieAnalyser.get_samples_for_movie(movie_id)
    resp = app.make_response(render_template('layout.html', words=words))
    resp.set_cookie("movie_id", movie_id)
    return resp


@app.route('/evaluate', methods=["POST"])
def evaluate():
    for elems in request.form:
        print(elems)
    print("Movie_id: ", request.cookies.get("movie_id"))
    return render_template('MoviePage.html')


def clever_function(id):
    print("clicked on :poster", id)
    return u"HELLO"


app.jinja_env.globals.update(clever_function=clever_function)

if __name__ == "__main__":
    app.run(debug=True)
