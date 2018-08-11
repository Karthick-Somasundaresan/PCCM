from flask import  Flask, render_template, request



app = Flask(__name__)


@app.route('/')
def index():
    return "Hello Flask"


@app.route('/home')
def home():
    movies = [{"poster":"./static/Pirates1.jpg", "name":" Pirates 1", "id": "asset1"},
              {"poster": "./static/Pirates1.jpg", "name": " Pirates 2", "id": "asset2"}]
    return render_template('HomePage.html', movies=movies)


@app.route('/surveyMovie')
def surveyMovie():
    movie_id = request.args.get('id')
    words = [u'trick', u'stole', u'ideas', u'pair', u'meaning', u'ambushing', u'betrayers', u'wreaked', u'buccaneer', u'bootstraps', u'plunder', u'gallivanting', u'extort', u'ravage', u'savvy', u'mutineers', u'feckless', u'brigandage', u'dauntless', u'hob']
    return render_template('layout.html', words=words)


@app.route('/evaluate', methods=["POST"])
def evalutate():
    for elems in request.form:
        print(elems)
    return render_template('MoviePage.html')

def clever_function(id):
    print("clicked on :poster", id)
    return u"HELLO"


app.jinja_env.globals.update(clever_function=clever_function)

if __name__ == "__main__":
    app.run(debug=True)
