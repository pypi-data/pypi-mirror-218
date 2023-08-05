from collections import defaultdict
from functools import update_wrapper
from time import time
from werkzeug.exceptions import TooManyRequests
from werkzeug.routing import RequestRedirect
from werkzeug.urls import url_parse
from werkzeug.wrappers import Response


class Limiter:
    def __init__(self, app=None):
        self.app = app
        self.enabled = app is not None
        self.limits = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.app.before_request(self.before_request)

    def before_request(self, request):
        if not self.enabled:
            return

        rule = self.get_rule(request)
        if rule is None:
            return

        endpoint = rule.endpoint
        limit = self.limits.get(endpoint)

        if limit is None:
            return

        ip = request.remote_addr
        limit_value = limit.get(ip)

        if limit_value is None:
            return

        limit_type = limit_value['type']
        limit_amount = limit_value['amount']
        limit_period = limit_value['period']
        limit_key = f'limiter:{limit_type}:{limit_amount}:{limit_period}:{ip}'

        current_time = int(time())
        limit_timestamp = self.app.redis.get(limit_key)

        if limit_timestamp is None:
            self.app.redis.setex(limit_key, limit_period, current_time)
        else:
            reset_time = int(limit_timestamp) + limit_period

            if reset_time > current_time:
                time_left = reset_time - current_time
                error_message = f'Too Many Requests. Try again in {time_left} seconds.'
                raise TooManyRequests(description=error_message)

            self.app.redis.setex(limit_key, limit_period, current_time)

    def get_rule(self, request):
        try:
            rule, _ = request.url_rule.rule, request.method
            return self.app.url_map.bind('').match(rule=rule, return_rule=True)[0]
        except RequestRedirect as e:
            endpoint = self.app.view_functions[e.new_url[0]]
            return self.app.url_map.bind('').match(endpoint=endpoint, return_rule=True)[0]
        except Exception:
            return None

    def limit(self, limit_type='default', amount=100, period=3600):
        def decorator(f):
            endpoint = f.__name__
            self.limits[endpoint][limit_type] = {'type': limit_type, 'amount': amount, 'period': period}
            return update_wrapper(f, decorator)

        return decorator
