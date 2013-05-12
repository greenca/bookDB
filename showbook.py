from twisted.web import resource, server
from mako.template import Template
import cgi
from database import Database

class ShowBook(resource.Resource):
	isLeaf = False
	def getChild(self, name, request):
		if name == '':
			return self
		return BookPage(name)
		
	def render_GET(self, request):
		username = request.getCookie('user')
		return self.write_form(username)
		
	def write_form(self, username):
		db = Database()
		fic = db.listBooks(username, 'fiction')
		nonfic = db.listBooks(username, 'nonfiction')
		myTemplate = Template(filename='templates/listbooks.html')
		return str(myTemplate.render(fic=fic, nonfic=nonfic))

		
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
		mytemplate = Template(filename='templates/bookinfo.html')
		return str(mytemplate.render(idnum=self.idnum, title=title, booktype=booktype, rating=rating, author=author, numpages=numpages, yearpub=yearpub, yearread=yearread, error=error))