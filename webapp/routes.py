from flask import Flask, render_template, request
import trials.MovieAnalyser as MovieAnalyser
import trials.UserScore as UserScore
import trials.scaleToUser as ScaleToUser


app = Flask(__name__, static_folder='./static')


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
    mov_id = request.cookies.get("movie_id")
    print("Movie_id: ", mov_id)
    usr_scr = UserScore.analyze_usr_scr(mov_id, request.form)
    print("User's evaluated Score:", usr_scr)
    print("Identifying hard words for the user")
    ScaleToUser.get_alternates(mov_id, usr_scr)
    mov_src = {
                "src": "./static/Movies/Pirates.of.the.Caribbean.Curse.of.the.Black.Pearl.2003.720p.BrRip.x264.Deceit.YIFY.mp4",
                "orig_titles": "./static/subtitles/original/Pirates_of_the_Caribbean_The_Curse_of_the_Black_Pearl.webvtt",
                "person_titles":"./static/subtitles/modified/Personalized_captions.vtt"
            }
    return render_template('MoviePage.html', mov_src=mov_src)

@app.route('/test')
def test():
    mov_src = {
                "src": "./static/Movies/Pirates.of.the.Caribbean.Curse.of.the.Black.Pearl.2003.720p.BrRip.x264.Deceit.YIFY.mp4",
                "orig_titles": "./static/subtitles/original/Pirates_of_the_Caribbean_The_Curse_of_the_Black_Pearl.webvtt",
                "person_titles":"./static/subtitles/modified/Personalized_captions.vtt"
            }
    return render_template('MoviePage.html', mov_src=mov_src)

def clever_function(id):
    print("clicked on :poster", id)
    return u"HELLO"


app.jinja_env.globals.update(clever_function=clever_function)

if __name__ == "__main__":
    app.run(debug=True)
