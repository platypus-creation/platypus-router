from webob.exc import HTTPMovedPermanently, HTTPTemporaryRedirect

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

def redirect(url, permanent=False):
    if permanent:
        return HTTPMovedPermanently(location=url)
    return HTTPTemporaryRedirect(location=url)