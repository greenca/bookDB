from twisted.web.resource import Resource
from mako.template import Template
from database import Database

class Login(Resource):
	isLeaf = False
	def getChild(self, name, request):
		return self

	def render_GET(self, request):
		return self.write_form()
    
	def render_POST(self, request):
		user = request.args['user'][0]
		password = request.args['password'][0]
		error = self.checkUser(user)
		if not error:
			error = self.checkPassword(user, password)
		if error:
			return self.write_form(user, error)
		
		request.addCookie('user', user)		
		mytemplate = Template(filename='templates/start.html')
		return str(mytemplate.render())


	def write_form(self, user='', error=''):
		mytemplate = Template(filename='templates/main.html')
		return str(mytemplate.render(user=user, error=error))
        
	def checkUser(self, user):
		error = ''
		db = Database()		
		res = db.getUser(user)
		if not res:
			error = 'Incorrect username or password'
		return error
		
	def checkPassword(self, user, pw):
		error = ''
		db = Database()
		res = db.checkPassword(user, pw)
		if not res:
			error = 'Incorrect username or password'
		return error
        
    
def html_escape(s):
	import cgi
	return cgi.escape(s)    
