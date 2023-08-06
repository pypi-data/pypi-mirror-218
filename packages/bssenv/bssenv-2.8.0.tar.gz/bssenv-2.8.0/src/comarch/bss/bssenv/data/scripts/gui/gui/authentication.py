'''This is only a very simple authentication example which stores session IDs in memory and does not do any password hashing.

Please see the `OAuth2 example at FastAPI <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>`_  or
use the great `Authlib package <https://docs.authlib.org/en/v0.13/client/starlette.html#using-fastapi>`_ to implement a real authentication system.

Here we just demonstrate the NiceGUI integration.
'''


from fastapi import Request
from .session import get_session_info


# in reality users and session_info would be persistent (e.g. database, file, ...) and passwords obviously hashed
users = [('user1', 'pass1'), ('user2', 'pass2')]


def is_authenticated(request: Request) -> bool:
    return (get_session_info(request.session.get('id')) or {}).get('authenticated', False)


def authenticate(session_id: str, username: str, password: str) -> bool:
    if (username.value, password.value) in users:
        get_session_info(session_id).update({'username': username.value, 'authenticated': True})
        return True
    return False
