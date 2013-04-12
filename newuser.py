from twisted.web import resource, server
from mako.template import Template
import cgi
import psycopg2

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
		if user == '':
			return self.write_form('', 'Please enter a username')		
		if password == '':
			return self.write_form(user, 'Please enter a password')
		if password != password2:
			return self.write_form(user, 'Passwords do not match')
		
		request.redirect('/')
		request.finish()
		return server.NOT_DONE_YET
		
		
	def write_form(self, user='', error=''):
		mytemplate = Template(filename='templates/newuser.html')
		return str(mytemplate.render(user=user, error=error))