import secrets
import time

SESSION_DURATION = 1800  # Session duration in seconds

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.secret_key = None

    def set_secret_key(self, secret_key):
        self.secret_key = secret_key

    def generate_session_id(self):
        return secrets.token_hex(16)

    def create_session(self):
        session_id = self.generate_session_id()
        session = {'_id': session_id, '_timestamp': time.time(), '_data': {}}
        self.sessions[session_id] = session
        return session_id

    def get_session(self, session_id):
        session = self.sessions.get(session_id)
        if session is not None and self.session_expired(session):
            self.destroy_session(session_id)
            session = None
        return session

    def session_expired(self, session):
        timestamp = session.get('_timestamp')
        return time.time() - timestamp > SESSION_DURATION

    def destroy_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def save_session(self, session):
        if session is not None:
            session['_timestamp'] = time.time()

    def update_session_data(self, session, data):
        session['_data'].update(data)

    def get_session_data(self, session):
        return session['_data']

session_manager = SessionManager()
