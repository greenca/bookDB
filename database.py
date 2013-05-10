import psycopg2

class Database():
	
	dbname = 'books'
			
	def connect(self):	
		self.conn = psycopg2.connect(database=self.dbname)
		self.cur = self.conn.cursor()
   
	def disconnect(self):
		self.conn.commit()
		self.cur.close()
		self.conn.close()

	def getUser(self, username):
		self.connect()
		self.cur.execute("SELECT username FROM users WHERE username = '%s';" % username)
		res = self.cur.fetchone()[0]
		self.disconnect()
		return res
		
	def addUser(self, username, password):
		self.connect()
		self.cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, password))
		self.disconnect()
		
	def checkPassword(self, username, password):
		self.connect()
		self.cur.execute("SELECT password FROM users WHERE username = '%s';" % username)
		res = self.cur.fetchone()[0]
		self.disconnect()
		return res == password
		
	def addBook(self, username, title, booktype, rating, author, numpages, yearpub, yearread):
		self.connect()
		self.cur.execute("INSERT INTO books (username, title, type, rating, author, numpages, yearpub, yearread) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (username, title, booktype, rating, author, numpages, yearpub, yearread))
		self.disconnect()
		
	def modBook(self, idnum, username, title, booktype, rating, author, numpages, yearpub, yearread):
		self.connect()
		self.cur.execute("UPDATE books SET title = %s, type = %s, rating = %s, author = %s, numpages = %s, yearpub = %s, yearread = %s WHERE id = %s AND username = %s;", (title, booktype, rating, author, numpages, yearpub, yearread, idnum, username))
		self.disconnect()
		
	def getBookInfo(self, idnum, username):
		self.connect()
		self.cur.execute("SELECT * FROM books WHERE id = %s AND username = '%s';" % (idnum, username))
		res = self.cur.fetchone()
		self.disconnect()
		return res
		
	



#cur.execute("INSERT INTO recipeinfo (title, meal, season, ingredients, time, cuisine, source, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (title,meal,season,mainingredient,preptime,cuisinetype,cookbook,rating))
#   cur.execute("SELECT currval('recipeinfo_id_seq');")
#   recipeid = cur.fetchone()[0]
#   cur.execute("INSERT INTO recipenotes (id, notes, filetype, filename) VALUES (%s, %s, %s, %s);", (recipeid,recipenotes,filetype,filename))
