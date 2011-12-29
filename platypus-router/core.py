from webob import Request, Response, exc
import re
from utils import singleton
from copy import deepcopy

class URLNotFound(Exception):
    pass

class Route(object):
    def __init__(self, regexp, action, urlvars, name):
        self.regexp = re.compile(regexp)
        self.action = action
        self.urlvars = urlvars
        self.name = name

@singleton
class Router(object):
    '''
    >>> router.add(r'^/$', 'actions.home')
    >>> router.add(r'^/blog/(?P<slug>[\w_-]+)/$', 'blog.actions.article')
    '''
    
    def __init__(self):
        self.routes = []

    def add(self, route_regexp, action, name=None, **urlvars):
        """
        Bind an route regexp to an action.
        
        router.add(r'^/hello/(?P<name>[\w_-]+)/$', 'hello_method')
        
        def hello_method(request, name):
            return 'Hello %s' % name
        """
        self.routes.append(Route(route_regexp, self.get_action(action), urlvars, name))
    
    def get_action(self, action):
        if isinstance(action, basestring):
            chunks = action.rsplit('.', 1)
            if len(chunks) > 1:
                module_name, func_name = chunks
                __import__(module_name)
                module = sys.modules[module_name]
            else:
                module = '__main__'
                func_name = chunks[0]
            action = getattr(module, func_name)
        return action
    
    def reverse(self, action, **urlvars):
        try:
            route = None
            if action in [route.name for route in self.routes if route.name is not None]:
                route = [route for route in self.routes if route.name == action][0]
            else:
                action = self.get_action(action)
                route = [route for route in self.routes if route.action == action][0]

            if route is not None:
                url = route.regexp.pattern.replace('^', '').replace('$', '')
                urlvars.update(route.urlvars)
                for key, value in urlvars.items():
                    url = re.sub(r'\(\?P<%s>[^\)]+\)' % key, str(value), url)
                return url
        except Exception, e:
            raise URLNotFound("Can't reverse %s with arguments %s" % (action, str(urlvars)), e)
        raise URLNotFound("Can't reverse %s with arguments %s" % (action, str(urlvars)))

    def __call__(self, environ, start_response):
        'Routing method'
        
        request = Request(environ)
        for route in self.routes:
            match = route.regexp.match(request.path_info)
            if match:
                request.urlvars = match.groupdict()
                request.urlvars.update(route.urlvars)
                try:
                    response = route.action(request, **request.urlvars)
                except exc.HTTPException, e:
                    response = e
      
                if isinstance(response, basestring):
                    response = Response(body=response)
                return response(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)

router = Router()
