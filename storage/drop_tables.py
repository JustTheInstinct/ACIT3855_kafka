from email import utils
import connexion
import swagger_ui_bundle
import sqlalchemy
import sqlite3

connection = sqlite3.connect("reviews.sqlite")
c = connection.cursor()

c.execute("""
            DROP TABLE review
        """)

c.execute("""
            DROP TABLE rating
        """)

connection.commit()
connection.close()