from twisted.web import resource, server
from mako.template import Template
import cgi
from database import Database
from datetime import date


class StatsHandler(resource.Resource):
	isLeaf = False
	def getChild(self, name, request):
		return self
	
	def render_GET(self, request):
		username = request.getCookie('user')
		if request.args:
			return self.write_form(username, firstyear = request.args[firstyear][0], lastyear = request.args[lastyear][0])
		return self.write_form(username)
		
	def write_form(self, username, firstyear=str(date.today().year), lastyear=str(date.today().year)):
		db = Database()
		avgRating = db.getAvgRating(username, firstyear, lastyear)
		totalPages = db.getTotalPages(username, firstyear, lastyear)
		avgPubYear = db.getAvgPubYear(username, firstyear, lastyear)
		mytemplate = Template(filename='templates/bookstats.html')
		return str(mytemplate.render(firstyear=firstyear, lastyear=lastyear, avgRating=avgRating, totalPages=totalPages, avgPubYear=avgPubYear))