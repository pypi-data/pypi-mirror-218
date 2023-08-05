import json
import asyncio
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from jinja2 import Environment, FileSystemLoader
from exceptions import HTTPException
from blueprints import Blueprint
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest, Unauthorized, Forbidden
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from itsdangerous import URLSafeTimedSerializer, BadSignature
from werkzeug.serving import run_simple
from werkzeug.urls import url_encode
import asyncio
from session import session_manager
from limiter import Limiter
import traceback
import os
import importlib.util

class Rust:
    def __init__(self):
        self.url_map = Map()
        self.error_handlers = {}
        self.before_request_funcs = []
        self.after_request_funcs = []
        self.template_env = Environment(loader=FileSystemLoader('templates'))
        self.host = '127.0.0.1'
        self.port = 8000
        self.debug = True
        self.view_functions = {}
        self.blueprints = []
        self.middlewares = []
        self.flash_messages = {}
        self.request_context = None
        self.static_folder = 'public'
        self.template_folder = 'templates'
        self.limiter = Limiter()
        self.config = {}
        self.configure_app()

    def route(self, rule, methods=['GET'], strict_slashes=False, secure=False):
        def decorator(f):
            endpoint = f.__name__
            self.url_map.add(Rule(rule, methods=methods, endpoint=endpoint, strict_slashes=strict_slashes))
            self.view_functions[endpoint] = f

            if secure:
                self.view_functions[endpoint] = self._secure_wrapper(self.view_functions[endpoint])

            return f
        return decorator

    def _secure_wrapper(self, view_func):
        async def secure_view(request, *args, **kwargs):
            if not request.is_secure:
                return Response('403 Forbidden - This route requires a secure (HTTPS) connection.', status=403)
            return await view_func(request, *args, **kwargs)
        return secure_view

    def errorhandler(self, code):
        def decorator(f):
            self.error_handlers[code] = f
            return f
        return decorator

    def configure_app(self):
        for key, value in self.config.items():
            setattr(self.jwt_manager, key, value)

    def before_request(self, f):
        self.before_request_funcs.append(f)
        return f

    def after_request(self, f):
        self.after_request_funcs.append(f)
        return f

    def use_middleware(self, middleware):
        self.middlewares.append(middleware)

    def register_blueprint(self, blueprint, options=None):
        blueprint.register(self, options)
        self.blueprints.append(blueprint)

    def create_app(self):
        app = DispatcherMiddleware(self.handle_not_found, {'/': self.dispatch_request})
        return app

    def run(self, host=None, port=None, debug=None):
        # Check if settings.py file is available
        settings_spec = importlib.util.find_spec('settings')
        if settings_spec:
            settings_module = importlib.util.module_from_spec(settings_spec)
            settings_spec.loader.exec_module(settings_module)
            if hasattr(settings_module, 'HOST'):
                self.host = settings_module.HOST
            if hasattr(settings_module, 'PORT'):
                self.port = settings_module.PORT
            if hasattr(settings_module, 'DEBUG'):
                self.debug = settings_module.DEBUG

        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if debug is not None:
            self.debug = debug

        run_simple(self.host, self.port, self, use_debugger=self.debug, use_reloader=self.debug)

    async def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = await self.dispatch_request(request)
        return response(environ, start_response)

    async def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            view_func = self.view_functions.get(endpoint)
            if view_func:
                request.blueprint = getattr(view_func, '__blueprint__', None)
                response = await self.process_request(request)
                if response is None:
                    response = await view_func(request, **values)
                response = await self.process_response(request, response)
            else:
                raise NotFound()
        except NotFound:
            response = self.handle_not_found(request)
        except MethodNotAllowed as e:
            return self.handle_method_not_allowed(e.valid_methods)
        except BadRequest as e:
            return self.handle_bad_request(request, e)
        except Forbidden as e:
            return self.handle_forbidden(request, e)
        except Unauthorized as e:
            return self.handle_unauthorized(request, e)
        except HTTPException as e:
            response = await self.handle_exception(e)
        return response
    
    def serve_static(self, path):
        static_path = os.path.join(self.static_folder, path)
        if os.path.exists(static_path):
            with open(static_path, 'rb') as f:
                response = self.response(f.read())
                response.headers['Content-Type'] = 'text/css' if path.endswith('.css') else 'text/javascript'
                return response
        return self.handle_not_found()

    def handle_not_found(self, request):
        error_template_path = os.path.join('errors', '404.html')
        if os.path.exists(error_template_path):
            with open(error_template_path, 'r') as f:
                error_template = f.read()
            return Response(error_template, status=404, content_type='text/html')
        else:
            return Response('404 Page not found', status=404)
        
    def handle_method_not_allowed(self, request):
        error_template_path = os.path.join('errors', '405.html')
        if os.path.exists(error_template_path):
            with open(error_template_path, 'r') as f:
                error_template = f.read()
            return Response(error_template, status=405, content_type='text/html')
        else:
            return Response('405 Method Not Allowed', status=405)

    def handle_error(self, error):
        traceback_message = traceback.format_exc()
        response = Response(traceback_message, status=500)
        return response

    def handle_bad_request(self, error):
        error_template_path = os.path.join('errors', '400.html')
        if os.path.exists(error_template_path):
            with open(error_template_path, 'r') as f:
                error_template = f.read()
            return Response(error_template, status=400, content_type='text/html')
        else:
            return Response('400 Bad Request', status=400)

    def handle_unauthorized(self, error):
        error_template_path = os.path.join('errors', '401.html')
        if os.path.exists(error_template_path):
            with open(error_template_path, 'r') as f:
                error_template = f.read()
            return Response(error_template, status=401, content_type='text/html')
        else:
            return Response('401 Unauthorized', status=401)

    def handle_forbidden(self, error):
        error_template_path = os.path.join('errors', '403.html')
        if os.path.exists(error_template_path):
            with open(error_template_path, 'r') as f:
                error_template = f.read()
            return Response(error_template, status=403, content_type='text/html')
        else:
            return Response('403 Forbidden', status=403)

    async def process_request(self, request):
        response = None  # Initialize the response variable
        for func in self.before_request_funcs:
            response = await func(request)
            if response is not None:
                return response

        # Add session handling
        session_id = request.cookies.get('session_id')
        if session_id:
            session = session_manager.get_session(session_id)
        else:
            session_id = session_manager.create_session()
            session = session_manager.get_session(session_id)
            response = Response()  # Initialize the response for new session
            response.set_cookie('session_id', session_id)

        request.session = session

        return response  # Return the response

    async def process_response(self, request, response):
        for func in self.after_request_funcs:
            response = await func(request, response)
        session_manager.save_session(request.session)
        return response

    async def handle_exception(self, e):
        if e.code in self.error_handlers:
            return await self.error_handlers[e.code](e)
        else:
            return Response('An error occurred.', status=500)

    def __call__(self, environ, start_response):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.wsgi_app(environ, start_response))


class VeloRequest(Request):
    @property
    def session(self):
        return session_manager.get_session(self.cookies.get('session_id'))

crust = Rust()
request = VeloRequest


def jsonify(data):
    return Response(json.dumps(data), mimetype='application/json')


def render_template(template_name, **context):
    template = crust.template_env.get_template(template_name)
    return Response(template.render(**context), mimetype='text/html')

def make_response(response):
    if isinstance(response, str):
        return Response(response)
    return response


def redirect(location):
    if location.startswith('/'):
        response = Response()
        response.headers['Location'] = location
        response.status_code = 302
        return response
    else:
        return Response('Invalid redirect location.', status=400)


def url_for(endpoint, **values):
    return crust.url_map.bind('').build(endpoint, values)


def send_file(filename, mimetype=None, as_attachment=False):
    response = Response()
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"' if as_attachment else f'inline; filename="{filename}"'
    if mimetype is not None:
        response.headers['Content-Type'] = mimetype
    return response


def redirect_args(location, *args, **kwargs):
    location = url_for(location, *args, **kwargs)
    return redirect(location)

def redirect_args(self, location, **kwargs):
        url = location
        if kwargs:
            query_params = url_encode(kwargs)
            url += f'?{query_params}'
        return Response(status=302, headers={'Location': url})

def send_from_directory(directory, filename):
    root = os.path.join(crust.static_folder, directory)
    return send_file(os.path.join(root, filename))


def url_rule(rule, view_func, **options):
    endpoint = options.pop("endpoint", None)
    crust.view_functions[endpoint] = view_func
    crust.url_map.add(Rule(rule, endpoint=endpoint, **options))


def stream_with_context(generator_or_function):
    response = Response(generator_or_function())
    response.headers.add("Transfer-Encoding", "chunked")
    return response


def stream_template(template_name, **context):
    template = crust.template_env.get_template(template_name)
    return Response(template.generate(**context), mimetype='text/html')


def scaffold(blueprint, static_folder=None, template_folder=None):
    if static_folder is not None:
        crust.static_folder = static_folder
    if template_folder is not None:
        crust.template_folder = template_folder
    crust.register_blueprint(blueprint)


def set_static_folder(static_folder):
    crust.static_folder = static_folder


def set_template_folder(template_folder):
    crust.template_folder = template_folder
    crust.template_env = Environment(loader=FileSystemLoader(template_folder))

def make_secure_token(self, salt=None, key=None):
        if salt is None:
            salt = self.config.get('SECRET_KEY', os.urandom(24))
        if key is None:
            key = os.urandom(16)
        serializer = URLSafeTimedSerializer(salt)
        return serializer.dumps(key)

def check_secure_token(self, token, salt=None):
    if salt is None:
        salt = self.config.get('SECRET_KEY', os.urandom(24))
    serializer = URLSafeTimedSerializer(salt)
    try:
        key = serializer.loads(token)
        return key
    except BadSignature:
        return None