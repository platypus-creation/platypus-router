from wsgiref.simple_server import make_server
from core import router

def runserver(router):
    server = make_server(router.host, router.port, router)
    print 'Starting server at %s:%s' % (router.host, router.port)
    server.serve_forever()
    

