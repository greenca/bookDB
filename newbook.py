from twisted.web import resource
from mako.template import Template
import cgi
from database import Database
from datetime import date

class NewBook(resource.Resource):
	isLeaf = False
	def getChild(self, name, request):
		if name=='':
			return self
		return Resource.getChild(self, name, request)
		
	def render_GET(self, request):
		return self.write_form()
		
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
		db.addBook(user, title, booktype, rating, author, numpages, yearpub, yearread)
		
		return 'User: ' + user + '<br>Title: ' + title + '<br>Type: ' + booktype + '<br>Rating: ' + rating + '<br>Author: ' + author + '<br>Number of Pages: ' + numpages + '<br>Year of Publication: ' + yearpub + '<br>Year Read: ' + yearread
		
	def write_form(self, title='', booktype='', rating='', author='', numpages='', yearpub='', yearread=str(date.today().year), error=''):
		fic = ''
		nonfic = ''		
		if booktype == 'fiction':
			fic = 'checked'
		elif booktype == 'nonfiction':
			nonfic = 'checked'			
		mytemplate = Template(filename='templates/book.html')
		return str(mytemplate.render(title=title, fic=fic, nonfic=nonfic, rating=rating, author=author, numpages=numpages, yearpub=yearpub, yearread=yearread, error=error))