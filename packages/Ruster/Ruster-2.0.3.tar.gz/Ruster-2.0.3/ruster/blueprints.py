from werkzeug.routing import Rule
from werkzeug.exceptions import NotFound


class Blueprint:
    def __init__(self, name, import_name, url_prefix=None):
        self.name = name
        self.import_name = import_name
        self.url_prefix = url_prefix
        self.deferred_functions = []

    def route(self, rule, methods=['GET'], strict_slashes=False, secure=True, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', f.__name__)
            self.deferred_functions.append((rule, endpoint, f, methods, strict_slashes, secure, options))
            return f
        return decorator

    def register(self, app, options=None):
        if options is None:
            options = {}
        for rule, endpoint, f, methods, strict_slashes, secure, view_options in self.deferred_functions:
            if self.url_prefix:
                rule = self.url_prefix + rule
            rule = Rule(rule, endpoint=endpoint, methods=methods, strict_slashes=strict_slashes, **view_options)
            app.url_map.add(rule)
            app.view_functions[endpoint] = f

    def view_function(self, endpoint):
        for rule, ep, f, methods, strict_slashes, secure, view_options in self.deferred_functions:
            if ep == endpoint:
                return f
        raise NotFound()
