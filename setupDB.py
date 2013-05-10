from database import Database

#import psycopg2

# Connect to an existing database
#conn = psycopg2.connect(database="books")

# Open a cursor to perform database operations
#cur = conn.cursor()

db = Database()
db.connect()

# Execute commands
#db.cur.execute("CREATE TABLE users (username varchar, password varchar);")

db.cur.execute("DROP TABLE books;")
db.cur.execute("CREATE TABLE books (id serial PRIMARY KEY, username varchar, title varchar, type varchar, rating decimal, author varchar, numpages int, yearpub int, yearread int);")

#db.cur.execute("DROP TABLE books;")
#db.cur.execute("CREATE TABLE books (username varchar, title varchar, type varchar, rating varchar, author varchar, numpages varchar, yearpub varchar, yearread varchar);")

# Make the changes to the database persistent
#conn.commit()

# Close communication with the database
#cur.close()
#conn.close()

db.disconnect()