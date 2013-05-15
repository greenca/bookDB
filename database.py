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
		res = self.cur.fetchone()
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
		if not rating:
			rating = 0
		if not numpages:
			numpages = 0
		if not yearpub:
			yearpub = 0
		if not yearread:
			yearread = 0
		self.connect()
		self.cur.execute("INSERT INTO books (username, title, type, rating, author, numpages, yearpub, yearread) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (username, title, booktype, rating, author, numpages, yearpub, yearread))
		self.cur.execute("SELECT currval('books_id_seq');")
		res = self.cur.fetchone()[0]
		self.disconnect()
		return res
		
	def modBook(self, idnum, username, title, booktype, rating, author, numpages, yearpub, yearread):
		if not rating:
			rating = 0
		if not numpages:
			numpages = 0
		if not yearpub:
			yearpub = 0
		if not yearread:
			yearread = 0
		self.connect()
		self.cur.execute("UPDATE books SET title = %s, type = %s, rating = %s, author = %s, numpages = %s, yearpub = %s, yearread = %s WHERE id = %s AND username = %s;", (title, booktype, rating, author, numpages, yearpub, yearread, idnum, username))
		self.disconnect()
		
	def getBookInfo(self, idnum, username):
		self.connect()
		self.cur.execute("SELECT * FROM books WHERE id = %s AND username = '%s';" % (idnum, username))
		res = self.cur.fetchone()
		self.disconnect()
		return res
		
	def listBooks(self, username, booktype):
		self.connect()
		self.cur.execute("SELECT id, title, rating FROM books WHERE username = '%s' AND type = '%s' ORDER BY rating DESC;" % (username, booktype))
		res = self.cur.fetchall()
		self.disconnect()
		return res
		
	def deleteBook(self, idnum, username):
		self.connect()
		self.cur.execute("DELETE FROM books WHERE id = %s and username = '%s';" % (idnum, username))
		self.disconnect()
		
	def searchBooks(self, username, criteria):
		self.connect()
		sql_req = "SELECT id, title, type, rating, author, numpages, yearpub, yearread FROM books WHERE username = '%s'" % username
		for c in criteria:
			if criteria[c][0]:
				sql_req += " AND " + c
				if c == 'title' or c == 'type' or c == 'author':
					sql_req += " ILIKE '%" + criteria[c][0] + "%'"
				elif criteria[c][0].count('-') == 1:
					rangevals = criteria[c][0].split('-')
					if rangevals[0]:				
						sql_req += " >= " + rangevals[0]
						if rangevals[1]:
							sql_req += " AND " + c + " <= " + rangevals[1]
					elif rangevals[1]:
						sql_req += " <= " + rangevals[1]
					else:
						ssql_req += " = " + criteria[c][0]
				else:
					sql_req += " = " + criteria[c][0] 
		sql_req += " ORDER BY rating DESC;"
		self.cur.execute(sql_req)
		res = self.cur.fetchall()
		self.disconnect()
		return res
		
	def getAvgRating(self, username, firstyear, lastyear):
		self.connect()
		self.cur.execute("SELECT avg(rating) FROM books WHERE username = '%s' AND yearread >= %s AND yearread <= %s;" % (username, firstyear, lastyear))
		res = self.cur.fetchone()[0]
		self.disconnect()
		return res
		
	def getTotalPages(self, username, firstyear, lastyear):
		self.connect()
		self.cur.execute("SELECT sum(numpages) FROM books WHERE username = '%s' AND yearread >= %s AND yearread <= %s;" % (username, firstyear, lastyear))
		res = self.cur.fetchone()[0]
		self.disconnect()
		return res
		
	def getAvgPubYear(self, username, firstyear, lastyear):
		self.connect()
		self.cur.execute("SELECT avg(yearpub) FROM books WHERE username = '%s' AND yearread >= %s AND yearread <= %s;" % (username, firstyear, lastyear))
		res = self.cur.fetchone()[0]
		self.disconnect()
		return res
	