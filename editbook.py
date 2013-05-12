from twisted.web import resource, server
from mako.template import Template
import cgi
from database import Database

class EditHandler(resource.Resource):
	isLeaf = False
	def getChild(self, name, request):
		if name == '':
			return self
		return BookPage(name)
		
	def render_GET(self, request):
		request.redirect('/')
		request.finish()
		return server.NOT_DONE_YET
		
		
class BookPage(resource.Resource):
	def __init__(self, idnum):
		resource.Resource.__init__(self)
		self.idnum = idnum
		
	def render_GET(self, request):
		username = request.getCookie('user')
		bookPage = self.getBookInfo(username)
		if bookPage:
			return bookPage
		request.redirect('/')
		request.finish()
		return server.NOT_DONE_YET
		
	def render_POST(self, request):
		error = ''
		user = cgi.escape(request.getCookie('user'))
		title = cgi.escape(request.args['title'][0])
		try:
			booktype = cgi.escape(request.args['type'][0])
		except:
			booktype = ''
			error = 'Select Fiction or Non-fiction'
		rating = cgi.escape(request.args['rating'][0])
		author = cgi.escape(request.args['author'][0])
		numpages = cgi.escape(request.args['numpages'][0])
		yearpub = cgi.escape(request.args['yearpub'][0])
		yearread = cgi.escape(request.args['yearread'][0])
		
		if not title:
			error = 'Book must have a title'
			
		if error:
			return self.write_form(title, booktype, rating, author, numpages, yearpub, yearread, error)		
				
		db = Database()
		db.modBook(self.idnum, user, title, booktype, rating, author, numpages, yearpub, yearread)
		
		request.redirect('/books/' + self.idnum)
		request.finish()
		return server.NOT_DONE_YET
		
	def getBookInfo(self, username):
		if self.idnum.isdigit():
			db = Database()
			bookinfo = db.getBookInfo(self.idnum, username)
			
			if bookinfo:
				title = bookinfo[2]
				booktype = bookinfo[3]
				rating = bookinfo[4]
				author = bookinfo[5]
				numpages = bookinfo[6]
				yearpub = bookinfo[7]
				yearread = bookinfo[8]
				
				return self.write_form(title, booktype, rating, author, numpages, yearpub, yearread)
				
		return None
		
	def write_form(self, title='', booktype='', rating='', author='', numpages='', yearpub='', yearread='', error=''):
		fic = ''
		nonfic = ''		
		if booktype == 'fiction':
			fic = 'checked'
		elif booktype == 'nonfiction':
			nonfic = 'checked'			
		mytemplate = Template(filename='templates/book.html')
		return str(mytemplate.render(title=title, fic=fic, nonfic=nonfic, rating=rating, author=author, numpages=numpages, yearpub=yearpub, yearread=yearread, error=error))