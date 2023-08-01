import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from song_store.db import get_db

bp = Blueprint('likedPlaylist', __name__)



@bp.route('/liked_playlist', methods=('GET', 'POST'))
def likedPlaylist():
    user_name = g.user['user_name']

    LIST_SONG_SQL = f"""
    SELECT s.song_id, s.song_name, s.energy, s.duration, s.release_date, alb.album_name, art.artist_name
    FROM Songs s, Albums alb, Artists art, Songs_to_artists s2a, Likes l, Users u
    WHERE s.album_id = alb.album_id AND
        s.song_id = s2a.song_id AND
        art.artist_id = s2a.artist_id AND
        u.user_name = ? AND
        l.song_id = s.song_id



    LIMIT 40
    """
    db = get_db() 
    try:
        songs = db.execute(LIST_SONG_SQL, [user_name]).fetchall()
    except Exception as error:
        print(error)
        return render_template('liked_playlist/noliked.html')
    return render_template('liked_playlist/playlist.html', songs=songs)

@bp.route('/deleteFromLikes', methods=(['POST']))
def deleteFromLikes():
    db = get_db()
    if request.method == 'POST':
        print(request.form['song_id'])
        DELETE_FROM_PLAYLIST = f"""DELETE FROM Likes WHERE user_name = ? AND song_id = ?"""

        db.execute(DELETE_FROM_PLAYLIST, (g.user['user_name'], request.form['song_id']))
        db.commit()

        print(g.user['user_name'])
    
    return render_template('recommender/addToLikes.html', added = False)
