from twisted.web import resource, server
from mako.template import Template
import cgi
from database import Database

class NewUser(resource.Resource):
	isLeaf = False
	def getChild(self, name, request):
		if name == '':
			return self
		return Resource.getChild(self, name, request)
		
	def render_GET(self, request):
		return self.write_form()
		
	def render_POST(self, request):
		user = request.args['user'][0]
		password = request.args['password'][0]
		password2 = request.args['password2'][0]
		error = self.checkUser(user)
		if error:
			return self.write_form('', error)
		error = self.checkPassword(password, password2)
		if error:		
			return self.write_form(user, error)
			
		db = Database()
		db.addUser(user, password)
		
		request.addCookie('user', user)		
		mytemplate = Template(filename='templates/start.html')
		return str(mytemplate.render())
		
		
	def write_form(self, user='', error=''):
		mytemplate = Template(filename='templates/newuser.html')
		return str(mytemplate.render(user=user, error=error))
		
	def checkUser(self, user):
		error = ''
		if user == '':
			error = 'Please enter a username'
		db = Database()		
		res = db.getUser(user)
		if res:
			error = 'Username is taken'
		return error
		
	def checkPassword(self, pw, pw2):
		error = ''
		if pw == '':
			error = 'Please enter a password'
		elif pw != pw2:
			error = 'Passwords do not match'
		return error