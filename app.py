from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from werkzeug.utils import redirect

from forms import MovieForm
from database import db
from models import Movies

app = Flask(__name__)

USED_DB = "postgresql"
USER_DB = "postgres"
USER_PASS = "admin"
DB_HOST = "localhost"
DATABASE = "cdp_db"

FINAL_URL = f"{USED_DB}://{USER_DB}:{USER_PASS}@{DB_HOST}/{DATABASE}"

app.config['SQLALCHEMY_DATABASE_URI'] = FINAL_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configuracion de Flask Migrate (Alembic)

migrate = Migrate()
migrate.init_app(app, db)

# Configuraicion flask wtf
app.config['SECRET_KEY'] = 'fb13ad0a-7e3e-4ab8-81cd-a33563abfdf0'

@app.route('/index')
@app.route('/')
def index():
    # movies = Movies.query.all()
    movies = Movies.query.order_by('id')
    movieCount = Movies.query.count()
    return render_template('index.html', movies=movies, movieCount=movieCount)

@app.route('/detail/<int:id>')
def detail(id):
    movie = Movies.query.get_or_404(id)
    return render_template('detail.html',movie=movie)

@app.route('/add', methods=['POST','GET'])
def addMovie():
    movie = Movies()
    movieForm = MovieForm(obj=movie)
    if request.method == 'POST':
        if movieForm.validate_on_submit():
            movieForm.populate_obj(movie)
            app.logger.debug(f'Pelicula a insertar: {movie}')
            # Insercion del nuevo registro
            db.session.add(movie)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return render_template('add.html', form = movieForm)


@app.route('/edit/<int:id>', methods=["POST","GET"])
def editMovie(id):
    movie = Movies.query.get_or_404(id)
    movieForm = MovieForm(obj=movie)
    if request.method == "POST":
        if movieForm.validate_on_submit():
            movieForm.populate_obj(movie)
            app.logger.debug(f'La persona a actualizar es: {movie}')
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('edit.html',form = movieForm)

@app.route('/remove/<int:id>')
def remove(id):
    movie = Movies.query.get_or_404(id)
    app.logger.debug(f'Persona a elminar: {movie}')
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))