from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from datetime import datetime

from song_store.auth import login_required
from song_store.db import get_db

bp = Blueprint('song', __name__)

LIST_SONG_SQL = """
SELECT *
FROM Songs s, Albums alb, Artists art, Songs_to_artists s2a
WHERE s.album_id = alb.album_id AND
      s.song_id = s2a.song_id AND
      art.artist_id = s2a.artist_id
ORDER BY score DESC
LIMIT 40
"""

COUNT_REMAINING_SONG_SQL = """
SELECT count(*) - 40 as num
FROM Songs
"""

LIST_REVIEW_SQL = """
SELECT user_name, rating, comment, date_made
FROM Reviews
WHERE song_id = ?
"""

NEW_OR_UPDATE_REVIEW_SQL = """
INSERT OR REPLACE INTO Reviews (user_name, song_id, rating, comment, date_made)
VALUES (?, ?, ?, ?, ?)
"""

DELETE_REVIEW_SQL = """
DELETE FROM Reviews 
WHERE user_name = ? AND
      song_id = ?
"""

@bp.route('/')
def list_songs():
    db = get_db()
    songs = db.execute(LIST_SONG_SQL).fetchall()
    num = db.execute(COUNT_REMAINING_SONG_SQL).fetchone()
    return render_template('song/list.html', songs=songs, remaining_num=num)


def new_or_update_review(db, request, song_id):
  # logic to handle POST
  user_name = g.user['user_name']
  rating = request.form['rating']
  comment = request.form['comment'].strip()
  date_made = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
  error = None
  
  # checks if input was entered properly
  if not comment:
    error = 'Must enter a comment'
  else:
    try:
      rating = int(rating)
    except ValueError:
      error = f'Rating {rating} should be an integer.'
    else:
      if rating < 0 or rating > 5:
        error = f'Rating must be within 0 <= x <= 5.'
  
  if error is None:
    db.execute(NEW_OR_UPDATE_REVIEW_SQL, (user_name, song_id, rating, comment, date_made))
    db.commit()
  else:
    flash(error)


def delete_review(db, song_id):
  db.execute(DELETE_REVIEW_SQL, (g.user['user_name'], song_id))
  db.commit()


@bp.route('/<song_id>/review', methods=('GET', 'POST'))
@login_required
def review(song_id):
    db = get_db()
    if request.method == 'POST':
      if request.form['action'] == 'delete':
        delete_review(db, song_id)
      else:
        new_or_update_review(db, request, song_id)

    reviews = db.execute(LIST_REVIEW_SQL, (song_id,)).fetchall()
    return render_template('song/review.html', reviews=reviews)

