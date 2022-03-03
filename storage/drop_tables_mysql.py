import mysql.connector, pymysql

connection = mysql.connector.connect(host="kafka1.eastus2.cloudapp.azure.com", user="user", password="password", database="events")
c = connection.cursor()

c.execute("""
            DROP TABLE review, rating
        """)

connection.commit()
connection.close()