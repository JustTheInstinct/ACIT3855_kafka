import sqlite3, mysql.connector, pymysql

connection = mysql.connector.connect(host="kafka1.eastus2.cloudapp.azure.com", user="user", password="password", database="events")
c = connection.cursor()

#c.execute("CREATE DATABASE events;")
c.execute("USE events;")

c.execute("""
            CREATE TABLE review
            (
            id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            review_id VARCHAR(40) NOT NULL,
            username VARCHAR(40) NOT NULL,
            comment VARCHAR(5000) NULL,
            rating INTEGER NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            trace_id INT NULL
            );
        """)

c.execute("""
            CREATE TABLE rating
            (
            id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            response_id VARCHAR(250) NOT NULL,
            user_rating BIT(1) NOT NULL,
            rate_count INTEGER NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            trace_id INT NULL
            );
        """)

connection.commit()
connection.close()