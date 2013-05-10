from twisted.web import resource
from mako.template import Template
import cgi
from database import Database

class ShowBook(resource.Resource):
	isLeaf = False
	def getChild(self, name, request):
		if name == '':
			return self
		return BookPage(name)
		
		
class BookPage(resource.Resource):
	def __init__(self, idnum):
		resource.Resource.__init__(self)
		self.idnum = idnum