from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
from login import Login
from newuser import NewUser
from newbook import NewBook
from editbook import EditHandler
from showbook import ShowBook
from printbook import PrintBook
from deletebook import DeleteBook
from searchbooks import SearchHandler
from displayStats import StatsHandler

resource = Login()
resource.putChild('register', NewUser())
resource.putChild('newbook', NewBook())
resource.putChild('edit', EditHandler())
resource.putChild('books', ShowBook())
resource.putChild('print', PrintBook())
resource.putChild('delete', DeleteBook())
resource.putChild('search', SearchHandler())
resource.putChild('stats', StatsHandler())

factory = Site(resource)
reactor.listenTCP(8090, factory)
reactor.run()
