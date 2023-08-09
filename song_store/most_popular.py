import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from song_store.db import get_db

bp = Blueprint('mostPopular', __name__)

GET_MOST_POPULAR = """
SELECT  *
FROM Songs S
INNER JOIN (
	SELECT L.song_id, COUNT(*) popularity
	FROM Likes L
	GROUP BY L.song_id
) ML ON S.song_id = ML.song_id
INNER JOIN Albums ALB ON ALB.album_id = S.album_id
INNER JOIN Songs_to_artists s2a ON s2a.song_id = S.song_id
INNER JOIN Artists ART ON ART.artist_id = s2a.artist_id
ORDER BY popularity DESC
LIMIT 50;

"""

@bp.route('/mostPopular', methods=(['GET']))
def mostPopular():
    db = get_db()
    if request.method == 'GET':
        songs = db.execute(GET_MOST_POPULAR).fetchall()
        return render_template('popular/most_popular.html', songs = songs)
