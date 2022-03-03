import sqlite3

connection = sqlite3.connect("reviews.sqlite")
c = connection.cursor()

c.execute("""
            CREATE TABLE review
            (
            id INTEGER PRIMARY KEY ASC NOT NULL,
            review_id VARCHAR(40) NOT NULL,
            username VARCHAR(40) NOT NULL,
            comment VARCHAR(5000) NULL,
            rating INTEGER NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            trace_id INTEGER
            )
        """)

c.execute("""
            CREATE TABLE rating
            (
            id INTEGER PRIMARY KEY ASC NOT NULL,
            response_id VARCHAR(250) NOT NULL,
            user_rating BIT(1) NOT NULL,
            rate_count INTEGER NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            trace_id INTEGER
            )
        """)

connection.commit()
connection.close()