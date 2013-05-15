from twisted.web import resource, server
from mako.template import Template
import cgi
from database import Database


class SearchHandler(resource.Resource):
	isLeaf = False
	def getChild(self, name, request):
		return self
	
	def render_GET(self, request):
		if request.args:
			username = request.getCookie('user')
			db = Database()
			books = db.searchBooks(username, request.args)
			mytemplate = Template(filename='templates/searchresults.html')
			return str(mytemplate.render(books=books))
		return self.write_form()
		
	def write_form(self, title='', booktype='', rating='', author='', numpages='', yearpub='', yearread='', error=''):
		fic = ''
		nonfic = ''		
		if booktype == 'fiction':
			fic = 'checked'
		elif booktype == 'nonfiction':
			nonfic = 'checked'			
		mytemplate = Template(filename='templates/searchbooks.html')
		return str(mytemplate.render(title=title, fic=fic, nonfic=nonfic, rating=rating, author=author, numpages=numpages, yearpub=yearpub, yearread=yearread, error=error))