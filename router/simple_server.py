from wsgiref.simple_server import make_server

def runserver(router):
    server = make_server(router.host, router.port, router)
    print 'Starting server at %s:%s' % (router.host, router.port)
    server.serve_forever()
    

