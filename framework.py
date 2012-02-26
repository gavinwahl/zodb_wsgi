import re
from jinja2 import Environment, FileSystemLoader


class HttpRequest(object):
    def __init__(self, environ):
        self.url = self.path = environ['PATH_INFO']
        if environ.get('QUERY_STRING'):
            self.url += '?' + environ['QUERY_STRING']

class HttpResponse(object):
    def __init__(self, content, headers = [('Content-Type', 'text/html'),], status = '200 Ok'):
        self.content = content
        self.headers = headers or []
        self.status = status

    def __iter__(self):
        yield self.content

class Http404(Exception):
    pass

class App(object):
    def __init__(self):
        self.routes = []

    def route(self, route, view=None):
        if view == None:
            def decorator(view):
                self.routes.append((route, view))
                return view
            return decorator
        else:
            self.routes.append((route, view))

    def get_view(self, request):
        for route, view in self.routes:
            match = re.compile(route + '$').match(request.path)
            if match:
                return (view, match.groups(), match.groupdict())
        return None

    def get_response(self, request):
        viewspec = self.get_view(request)
        if not viewspec:
            raise Http404
        view, args, kwargs = viewspec
        return view(request, *args, **kwargs)

    def application(self, environ, start_response):
        request = HttpRequest(environ)
        response = self.get_response(request)
        start_response(response.status, response.headers)
        return response

    __call__ = application

    def render(self, request, template, env={}):
        jinja_env = Environment(
                loader=FileSystemLoader(self.template_path),
                extensions=['jinja2.ext.autoescape'],
                autoescape=True,
                )
        template = jinja_env.get_template(template)
        return HttpResponse(str(template.render(env, request=request, vars=vars)))
