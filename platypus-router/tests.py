import unittest
from core import router, URLNotFound
from webob import Request, Response, exc

class TestRouter(unittest.TestCase):

    def setUp(self):
        def hello_method(request, name, template='Hello %s'):
            return template % name
        self.hello_method = hello_method
        
    def test_add_route(self):
        self.assertEqual(0, len(router.routes))

        router.add(r'^/hello/(?P<name>[\w_-]+)/$', self.hello_method)
        self.assertEqual(1, len(router.routes))

        router.add(r'^/hello/my/name/is/(?P<name>[\w_-]+)/$', self.hello_method, template='Hello my name is %s')
        self.assertEqual(2, len(router.routes))

    def test_reverse(self):
        router.add(r'^/hello/(?P<name>[\w_-]+)/$', self.hello_method)
        router.add(r'^/hello/my/name/is/(?P<name>[\w_-]+)/$', self.hello_method, template='Hello my name is %s', name='hello_my_name_is')
        
        self.assertEqual('/hello/Vincent/', router.reverse(self.hello_method, name='Vincent'))
        self.assertEqual('/hello/my/name/is/Vincent/', router.reverse('hello_my_name_is', name='Vincent'))

        try:
            router.reverse('does.not.exist')
            self.fail()
        except URLNotFound:
            pass
            
    
    def test_route(self):
        def start_response(status, headers):
            pass
            # return Response(status=status, headers)
        router.add(r'^/hello/(?P<name>[\w_-]+)/$', self.hello_method)
        router.add(r'^/hello/my/name/is/(?P<name>[\w_-]+)/$', self.hello_method, template='Hello my name is %s', name='hello_my_name_is')
        self.assertEqual(['Hello Vincent'], router(Request.blank('http://localhost/hello/Vincent/').environ, start_response))
        self.assertEqual(['Hello my name is Vincent'], router(Request.blank('http://localhost/hello/my/name/is/Vincent/').environ, start_response))
        self.assertEqual(exc.HTTPNotFound()(Request.blank('http://localhost/does/not/exists/').environ, start_response), router(Request.blank('http://localhost/does/not/exists/').environ, start_response))
        
    def tearDown(self):
        router.routes = []

if __name__ == '__main__':
    unittest.main()
