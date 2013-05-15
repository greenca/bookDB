from twisted.web import resource, server
from mako.template import Template
import cgi
from database import Database


class DeleteBook(resource.Resource):
	isLeaf = False
	
	def __init__(self):
		resource.Resource.__init__(self)
		self.putChild('confirm', ConfirmDelete())
		
	def getChild(self, name, request):
		if name == '':
			return self
		return DeleteRequest(name)
		
	def render_GET(self, request):
		request.redirect('/')
		request.finish()
		return server.NOT_DONE_YET
		
		
class DeleteRequest(resource.Resource):
	
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
		mytemplate = Template(filename='templates/deletebook.html')
		return str(mytemplate.render(idnum=self.idnum, title=title, booktype=booktype, rating=rating, author=author, numpages=numpages, yearpub=yearpub, yearread=yearread, error=error))
	
	
class ConfirmDelete(resource.Resource):
	def getChild(self, name, request):
		if name == '':
			return self
		return DeletePage(name)
		
	def render_GET(self, request):
		request.redirect('/')
		request.finish()
		return server.NOT_DONE_YET
		
		
class DeletePage(resource.Resource):
	def __init__(self, idnum):
		resource.Resource.__init__(self)
		self.idnum = idnum
		
	def render_GET(self, request):
		if not self.idnum.isdigit():
			request.redirect('/')
			request.finish()
			return server.NOT_DONE_YET
		username = request.getCookie('user')
		db = Database()
		db.deleteBook(self.idnum, username)
		request.redirect('/books')
		request.finish()
		return server.NOT_DONE_YET