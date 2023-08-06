from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import ui
from ..authentication import is_authenticated, authenticate
from ..session import start_new_session, clear_session


@ui.page('/login')
def login(request: Request) -> None:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if authenticate(session_id, username, password):
            ui.open('/')
        else:
            ui.notify('Wrong username or password', color='negative')

    if is_authenticated(request):
        return RedirectResponse('/')
    session_id = start_new_session(request)
    with ui.card().classes('absolute-center'):
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password').props('type=password').on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)


@ui.page('/logout')
def logout(request: Request) -> None:
    if is_authenticated(request):
        clear_session(request)
        return RedirectResponse('/login')
    return RedirectResponse('/')
