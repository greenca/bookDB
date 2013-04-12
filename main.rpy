from twisted.web import resource, server
from mako.template import Template


class Main(resource.Resource):
    isLeaf = False
    def getChild(self, name, request):
        return self

    def render_GET(self, request):
        return self.write_form()
    
    def render_POST(self, request):
        user = request.args['user'][0]
        password = request.args['password'][0]
        return self.write_form(user, 'Incorrect login information')
            
    
    def write_form(self, user='', error=''):
        mytemplate = Template(filename='templates/main.html')
        return str(mytemplate.render(user=user, error=error))
        
    
def html_escape(s):
    import cgi
    return cgi.escape(s)    

resource = Main()
