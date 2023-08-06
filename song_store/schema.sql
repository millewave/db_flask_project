CREATE TABLE IF NOT EXISTS "Songs" (
	"song_id"	TEXT UNIQUE,
	"album_id"	TEXT,
	"song_name"	TEXT,
	"explicit"	TEXT,
	"danceability"	REAL,
	"energy"	REAL,
	"speechiness"	REAL,
	"acousticness"	REAL,
	"instrumentalness"	REAL,
	"liveness"	REAL,
	"valence"	REAL,
	"tempo"	REAL,
	"duration"	INTEGER,
	"release_date"	TEXT,
	"score" REAL,
	PRIMARY KEY("song_id")
);

CREATE TABLE IF NOT EXISTS "Albums" (
	"album_id"	TEXT NOT NULL UNIQUE,
	"album_name"	TEXT NOT NULL,
	PRIMARY KEY("album_id")
);

CREATE TABLE IF NOT EXISTS "Artists" (
	"artist_id"	TEXT NOT NULL UNIQUE,
	"artist_name"	TEXT NOT NULL,
	PRIMARY KEY("artist_id")
);

CREATE TABLE IF NOT EXISTS "Likes" (
	"user_name"	TEXT NOT NULL,
	"song_id"	TEXT NOT NULL,
	FOREIGN KEY("user_name") REFERENCES "Users"("user_name"),
	FOREIGN KEY("song_id") REFERENCES "Songs"("song_id"),
	PRIMARY KEY("user_name", "song_id")
);

CREATE TABLE IF NOT EXISTS "Reviews" (
	"user_name"	TEXT NOT NULL,
	"song_id"	TEXT NOT NULL,
	"rating"	INTEGER,
	"comment"	TEXT,
	"date_made"	TEXT,
	FOREIGN KEY("user_name") REFERENCES "Users"("user_name"),
	FOREIGN KEY("song_id") REFERENCES "Songs"("song_id"),
  PRIMARY KEY("user_name", "song_id")
);

CREATE TABLE IF NOT EXISTS "Songs_to_artists" (
	"artist_id"	TEXT NOT NULL,
	"song_id"	TEXT NOT NULL,
	PRIMARY KEY("artist_id", "song_id"),
	FOREIGN KEY("artist_id") REFERENCES "Artists"("artist_id"),
	FOREIGN KEY("song_id") REFERENCES "Songs"("song_id")
);

CREATE TABLE IF NOT EXISTS "Users" (
	"user_name"	TEXT PRIMARY KEY NOT NULL,
	"age"	INTEGER,
	"password" TEXT NOT NULL
);
