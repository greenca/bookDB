import psycopg2

# Connect to an existing database
conn = psycopg2.connect(database="books")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute commands
cur.execute("CREATE TABLE users (username varchar, password varchar);")

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()