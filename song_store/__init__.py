import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'song_store.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    # @app.route('/')
    # def index():
    #     return 'Song Store Project in construction ...'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)    

    from . import song
    app.register_blueprint(song.bp)
    app.add_url_rule('/', endpoint='list_songs')

    from . import recommender
    app.register_blueprint(recommender.bp)
    app.add_url_rule('/', endpoint='recommender')
    app.add_url_rule('/', endpoint='recommendation')
    app.add_url_rule('/', endpoint='addToLikes')

    from . import liked_playlist
    app.register_blueprint(liked_playlist.bp)

    from . import most_popular
    app.register_blueprint(most_popular.bp)
    app.add_url_rule('/', endpoint="mostPopular")




    
    return app
