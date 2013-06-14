from database import Database

db = Database()
db.connect()

db.cur.execute("CREATE TABLE books (id serial PRIMARY KEY, username varchar, title varchar, type varchar, rating decimal, author varchar, numpages int, yearpub int, yearread int);")
db.cur.execute("CREATE TABLE users (username varchar, password varchar);")




for r in open('/home/green/JAC_book_DB/fiction.csv'):
	val = r.split('"')
	if val[1]:
		title = val[1].replace("'","''")
		rating = val[3]
		print 'Title: ' + val[1] + ', Rating: ' + val[3]
		db.cur.execute("INSERT INTO books ( username, title, type, rating, numpages, yearpub, yearread ) VALUES ( '%s', '%s', '%s', %s, %s, %s, %s );" % ('John', title, 'fiction', rating, 0, 0, 0))
		
for r in open('/home/green/JAC_book_DB/nonfiction.csv'):
	val = r.split('"')
	if val[1]:
		title = val[1].replace("'","''")
		rating = val[2].replace(',','')
		print 'Title: ' + val[1] + ', Rating: ' + rating
		db.cur.execute("INSERT INTO books ( username, title, type, rating, numpages, yearpub, yearread ) VALUES ( '%s', '%s', '%s', %s, %s, %s, %s );" % ('John', title, 'nonfiction', rating, 0, 0, 0))
		
		
db.disconnect()