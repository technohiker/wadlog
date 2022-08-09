# API Calls:
-  ## SEARCH:
    -   Call
    -   ID
    -   Title
    -   Size
    -   Date
    -   Author
    -   Description
    -   Rating
    -   Votes
    -   URL
    -   
-   ## GET:
    -   Gets file information by ID.  Uses the same parameters as above to update mod info.

# Schema Design:
-   ## Mods:
    -   ID SERIAL PRIMARY KEY,
    -   Title TEXT NOT NULL,
    -   File-ID INTEGER NOT NULL,
    -   URL TEXT NOT NULL,
    -   Description TEXT,
    -   Date Uploaded TIMESTAMP NOT NULL,
    -   Date Updated TIMESTAMP NOT NULL,
    -   Author TEXT NOT NULL,
    -   Category TEXT NOT NULL,(pull from idgamesurl or URL, requires   substring)
    -   Rating INTEGER,
    -   Rating Count INTEGER NOT NULL
-   ## Users:
    -   ID SERIAL PRIMARY KEY,
    -   Username TEXT NOT NULL,
    -   Email TEXT NOT NULL,
    -   Password TEXT NOT NULL,
    -   Date Joined TIMESTAMP NOT NULL,
    -   Profile Picture TEXT
-   ## User-Mods:
    -   ID SERIAL PRIMARY KEY,
    -   User ID INTEGER FOREIGN KEY,
    -   Mod ID INTEGER FOREIGN KEY,
    -   Date Added TIMESTAMP NOT NULL,
    -   User Review TEXT,
    -   User Notes TEXT,
    -   Play Status TEXT,
    -   Now Playing BOOLEAN NOT NULL
-   ## User Log:
    -   ID SERIAL PRIMARY KEY,
    -   User-Mod ID INTEGER FOREIGN KEY,
    -   Date Added, TIMESTAMP,
    -   Activity Type(rating, started playing, added mod, etc.)
    -   Description(Pre-written description describing what happened
                    ex. "User rated this mod 4 stars" or "user just removed this mod.") TEXT NOT NULL
-   ## Comment:
    -   ID SERIAL PRIMARY KEY,
    -   User ID INTEGER FOREIGN KEY,
    -   Target User INTEGER FOREIGN KEY,
    -   Timestamp, TIMESTAMP NOT NULL
    -   Text, TEXT NOT NULL
-   ## Questions:
    -   What is the best way of handling the record vs each log of a record?


# Image Sources:
-   Default user image: https://feedback.seekingalpha.com/s/cache/8d/84/8d844a1bb966f7012aec20276f0e4283.png

# Lessons Learned:
-   Secondary argument of SQLAlchemy relationships should only be used if many-to-many table exists solely to connect two tables together.
-   Do not make names of models so similar.  Will cause confusion.