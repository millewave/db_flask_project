# Abstract
README for song_store package.

# Environment
This project requires Flask 2.3.x. Use ```flask --version``` to check. If you need to upgrade flask, run ```pip install --upgrade Flask```.

If you find you do need to upgrade Flask, chances are you will also need to upgrade the watchdog package, in which case, run ```pip install --upgrade watchdog```.

# Database
Please see [schema.sql](./song_store/schema.sql) for database schema.

We have prepopulated more than one millons Spotify songs as well as hundreds of thousands of albums and artists. If you would like to utilize the data, please contact the authors to download the song_store.sqlite into [instance](./instance/).

# Main UX Pages
Flask app run by default hosts the webpage at http://127.0.0.1:5000. Please navigate to it and enjoy.

# Notes
Quick notes on operational steps

Run the application.
```
flask --app song_store run
```

# References
[Flask 2.3.x Tutorial](https://flask.palletsprojects.com/en/2.3.x/tutorial/factory/)
