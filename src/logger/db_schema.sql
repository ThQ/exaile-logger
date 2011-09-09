CREATE TABLE _info (
    name TEXT,
    value TEXT,
    PRIMARY KEY(name),
    UNIQUE(name)
);

CREATE TABLE history (
    id INTEGER NOT NULL,
    date INTEGER NOT NULL,
    file_url TEXT,
    song_artist TEXT,
    song_album TEXT,
    song_title TEXT,
    song_length REAL,
    listened_for REAL,
    listening_ratio REAL,
    PRIMARY KEY(id),
    UNIQUE(id)
);
