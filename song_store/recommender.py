import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from song_store.db import get_db

bp = Blueprint('recommender', __name__)

@bp.route('/recommender', methods=('GET', 'POST'))
def recommender():
    options = {
        "Dancebility": ["Not", "Below Average", "Don't Care", "Above Average", "Very"],
        "Energy": ["Not", "Below Average", "Don't Care", "Above Average", "Very"],
        "Electronic": ["Not", "Below Average", "Don't Care", "Above Average", "Very"],
        "Live": ["Not", "Below Average", "Don't Care", "Above Average", "Very"],
        "Happy": ["Not", "Below Average", "Don't Care", "Above Average", "Very"],  
    }
    
    adult = True
    selected_values = {}
    bpm = None
    duration = None
    release_year = None

    if request.method == 'POST':
        explicit = bool(request.form.get('explicit', True))
        for header in options:
            selected_values[header] = request.form.get(header)
        bpm = request.form.get('bpm')
        duration = request.form.get('duration')
        release_year = request.form.get('release_year')

        query_params = {
            'bpm': bpm,
            'duration': duration,
            'release_year': release_year,
            'selected_values': selected_values,
            'explicit': explicit,
        }

        return redirect(url_for('recommender.recommendation', **query_params))



    return render_template('recommender/recommender.html', options=options, adult=adult, selected_values=selected_values, bpm=bpm, duration=duration, release_year=release_year)



@bp.route('/recommendation')
def recommendation():
    # Retrieve the data from query parameters
    bpm = request.args.get('bpm')
    duration = request.args.get('duration')
    release_year = request.args.get('release_year')
    selected_values = request.args.get('selected_values')
    explicit = request.args.get('explicit')
    if explicit == True:
        explicitString = "True"
    else:
        explicitString = "False"

    print(explicitString)
    #Render table
    db = get_db()
    #TODO CHANGE SQL AND MAKE SURE ALREADY LIKED VALUES FOR THE USER DO NOT SHOW UP
    RECOMMENDED_SONGS = f"""
    SELECT s.song_id, s.song_name, s.energy, s.duration, s.release_date, alb.album_name, art.artist_name
    FROM Songs s, Albums alb, Artists art, Songs_to_artists s2a
    WHERE s.album_id = alb.album_id AND
        s.song_id = s2a.song_id AND
        art.artist_id = s2a.artist_id AND
        s.explicit = '{explicitString}'

    LIMIT 40

    """
    songs = db.execute(RECOMMENDED_SONGS).fetchall()
    


    #Add to likes



    # Your result page rendering code here
    return render_template('recommender/recommendation.html', songs=songs)


@bp.route('/addToLikes', methods=(['POST']))
def addToLikes():
    db = get_db()
    if request.method == 'POST':
        print(request.form['song_id'])
        INSERT_INTO_PLAYLIST = f"""INSERT INTO Likes (user_name, song_id) VALUES (?, ?)"""

        db.execute(INSERT_INTO_PLAYLIST, (g.user['user_name'], request.form['song_id']))
        db.commit()

        print(g.user['user_name'])
    
    return render_template('recommender/addToLikes.html', added = True)
