import uuid
from typing import Dict
from fastapi import Request


session_info: Dict[str, Dict] = {}


def get_session_info(session_id: str) -> Dict:
    return session_info.get(session_id, None)


def start_new_session(request: Request) -> str:
    session_id = str(uuid.uuid4())
    request.session['id'] = session_id  # NOTE this stores a new session ID in the cookie of the client
    session_info[session_id] = {}
    return session_id


def clear_session(request: Request) -> None:
    session_info.pop(request.session['id'])
    request.session['id'] = None
