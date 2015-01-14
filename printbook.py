from twisted.web import resource, server
from mako.template import Template
import cgi
from database import Database

class PrintBook(resource.Resource):
	isLeaf = False
	def getChild(self, name, request):
                return self
		
	def render_GET(self, request):
		username = request.getCookie('user')
		return self.write_form(username)
		
	def write_form(self, username):
		db = Database()
		fic = db.listBooks(username, 'fiction')
		nonfic = db.listBooks(username, 'nonfiction')
		myTemplate = Template(filename='templates/printbooks.html')
		return str(myTemplate.render(fic=fic, nonfic=nonfic))
