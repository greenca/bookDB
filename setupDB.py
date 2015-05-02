from database import Database

db = Database()
db.connect()

db.cur.execute("DROP TABLE books;")
db.cur.execute("CREATE TABLE books (id serial PRIMARY KEY, username varchar, title varchar, type varchar, rating decimal, author varchar, numpages int, yearpub int, yearread int);")

db.disconnect()
