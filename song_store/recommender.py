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
        "How do you feel about songs that are easy to dance to?": ["Strongly Dislike", "Dislike", "Don't Care", "Prefer", "Strongly Prefer"],
        "How do you feel about high-energy songs?": ["Strongly Dislike", "Dislike", "Don't Care", "Prefer", "Strongly Prefer"],
        "How do you feel about acoustic songs?": ["Strongly Dislike", "Dislike", "Don't Care", "Prefer", "Strongly Prefer"],
        "How do you feel about live-recorded songs?": ["Strongly Dislike", "Dislike", "Don't Care", "Prefer", "Strongly Prefer"],
        "How do you feel about a happy song?": ["Strongly Dislike", "Dislike", "Don't Care", "Prefer", "Strongly Prefer"],  
        "How do you feel about a fast song?": ["Strongly Dislike", "Dislike", "Don't Care", "Prefer", "Strongly Prefer"],
        "How do you feel about a long song?": ["Strongly Dislike", "Dislike", "Don't Care", "Prefer", "Strongly Prefer"],  
        "How do you feel about a song released recently?": ["Strongly Dislike", "Dislike", "Don't Care", "Prefer", "Strongly Prefer"],  
    }
    
    adult = True
    selected_values = {}
    numSongsRequested = None

    if request.method == 'POST':
        explicit = bool(request.form.get('explicit', True))
        for header in options:
            selected_values[header] = request.form.get(header)
        numSongsRequested = request.form.get('numSongsRequested')

        query_params = {
            'numSongsRequested': numSongsRequested,
            'selected_values': selected_values,
            'explicit': explicit,
        }

        return redirect(url_for('recommender.recommendation', **query_params))



    return render_template('recommender/recommender.html', options=options, adult=adult, selected_values=selected_values, numSongsRequested = numSongsRequested)



@bp.route('/recommendation')
def recommendation():
    # Retrieve the data from query parameters
    user_name = g.user['user_name']
    numSongsRequested = request.args.get('numSongsRequested')
    selected_values = request.args.get('selected_values')
    explicit = request.args.get('explicit')
    if explicit == True:
        explicitString = "True"
    else:
        explicitString = "False"
    numSongs = 0
    try:
        numSongs = int(numSongsRequested)
        if numSongs>50:
            numSongs = 50
    except ValueError:
        numSongs = 20
    print(explicitString)
    print(selected_values)
    print(type(selected_values))
    #Render table
    db = get_db()
    scalars = createScalars(eval(selected_values))
    #TODO CHANGE SQL AND MAKE SURE ALREADY LIKED VALUES FOR THE USER DO NOT SHOW UP
    db.execute("ALTER TABLE Songs DROP COLUMN score")
    ALTER_SONGS = f"""
               ALTER TABLE Songs 
               ADD score REAL AS ('{scalars[0]}'*danceability + '{scalars[1]}'*energy + '{scalars[2]}'*acousticness + '{scalars[3]}'*liveness + '{scalars[4]}'*valence + '{scalars[5]}'*tempo + '{scalars[6]}'*duration)"""
    db.execute(ALTER_SONGS)
    RECOMMENDED_SONGS = f"""
    SELECT s.song_id, s.song_name, s.energy, s.duration, s.release_date, s.score, alb.album_name, art.artist_name
    FROM Songs s, Albums alb, Artists art, Songs_to_artists s2a
    WHERE s.album_id = alb.album_id AND
        s.song_id = s2a.song_id AND
        art.artist_id = s2a.artist_id AND
        s.explicit = '{explicitString}' AND
        s.song_id NOT IN (
            SELECT l.song_id
            FROM Likes l, Users u
            WHERE u.user_name = ? AND
                l.user_name = u.user_name
        )
    ORDER BY score DESC
    LIMIT '{numSongs}'

    """
    songs = db.execute(RECOMMENDED_SONGS, [user_name]).fetchall()
    


    #Add to likes



    # Your result page rendering code here
    return render_template('recommender/recommendation.html', songs=songs)


def createScalars(dict):
    scalars = []
    for key, value in dict.items():
        if value == None:
            scalars.append(0)
        elif value == "Strongly Dislike":
            scalars.append(-2)
        elif value == "Dislike":
            scalars.append(-1)
        elif value == "Don't Care":
            scalars.append(0)
        elif value == "Prefer":
            scalars.append(1)
        elif value == "Strongly Prefer":
            scalars.append(2)
    return scalars
            


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
