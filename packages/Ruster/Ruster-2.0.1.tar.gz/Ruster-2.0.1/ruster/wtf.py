import jwt
from datetime import datetime, timedelta
from werkzeug.datastructures import MultiDict
from functools import wraps

class WTF:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate_csrf_token(self):
        payload = {'exp': datetime.utcnow() + timedelta(hours=1)}
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def validate_csrf_token(self, token):
        try:
            decoded_token = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            expiration = datetime.fromtimestamp(decoded_token['exp'])
            if datetime.utcnow() <= expiration:
                return True
        except (jwt.InvalidTokenError, KeyError):
            pass
        return False

    def form(self, formdata=None, **kwargs):
        return GoRouteWTFForm(self, formdata, **kwargs)


class GoRouteWTFField:
    def __init__(self, validators=None):
        self.validators = validators or []

    def validate(self, form, field):
        for validator in self.validators:
            validator(form, field)


class GoRouteWTFStringField(GoRouteWTFField):
    def __init__(self, label=None, validators=None):
        super().__init__(validators)
        self.label = label

    def process_data(self, value):
        return value

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0]
        else:
            self.data = ''

    def __call__(self, **kwargs):
        return f'<input type="text" name="{kwargs.get("name", "")}" value="{kwargs.get("value", "")}" {"".join(f"{k}='{v}'" for k, v in kwargs.items())}>'


class GoRouteWTFForm:
    def __init__(self, gotroutewtf, formdata=None, **kwargs):
        self.fields = []
        self.gotroutewtf = gotroutewtf
        self.process(formdata)

    def process(self, formdata=None):
        if formdata is None:
            formdata = MultiDict()

        for field in self.fields:
            field.process_formdata(formdata.getlist(field.name))

    def validate(self):
        return all(field.validate(self, field) for field in self.fields)

    def hidden_tag(self):
        token = self.gotroutewtf.generate_csrf_token()
        return f'<input type="hidden" name="csrf_token" value="{token.decode()}">'

    def populate_obj(self, obj):
        for name, field in self._fields.items():
            setattr(obj, name, field.data)

    @property
    def data(self):
        data = {}
        for name, field in self._fields.items():
            data[name] = field.data
        return data
