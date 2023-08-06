#!/usr/bin/env python3

import os
from starlette.middleware.sessions import SessionMiddleware
from nicegui import app, ui
from gui import pages


# put your your own secret key in an environment variable MY_SECRET_KEY
app.add_middleware(SessionMiddleware, secret_key=os.environ.get('MY_SECRET_KEY', ''))


ui.run()
