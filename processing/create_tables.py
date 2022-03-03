import sqlite3

connection = sqlite3.connect("stats.sqlite")
c = connection.cursor()

c.execute("""
            CREATE TABLE stats
            (
            id INTEGER PRIMARY KEY ASC NOT NULL,
            num_of_ratings INTEGER NOT NULL,
            num_positive INTEGER,
            num_negative INTEGER,
            timestamp VARCHAR(100) NOT NULL,
            trace_id INTEGER
            )
        """)

connection.commit()
connection.close()