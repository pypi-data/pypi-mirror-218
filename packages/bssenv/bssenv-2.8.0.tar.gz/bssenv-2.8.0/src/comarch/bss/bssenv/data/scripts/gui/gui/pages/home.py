from typing import Dict
from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import ui
from ..authentication import is_authenticated
# from .session import get_session_info


tab_names = ['A', 'B', 'C']


@ui.page('/')
def home_page(request: Request) -> None:
    if not is_authenticated(request):
        return RedirectResponse('/login')
    # session = get_session_info(request.session['id'])
    # with ui.column().classes('absolute-center items-center'):
    #     ui.label(f'Hello {session["username"]}!').classes('text-2xl')
    #     # NOTE we navigate to a new page here to be able to modify the session cookie (it is only editable while a request is en-route)
    #     # see https://github.com/zauberzeug/nicegui/issues/527 for more details
    #     ui.button('', on_click=lambda: ui.open('/logout')).props('outline round icon=logout')

    def switch_tab(msg: Dict) -> None:
        name = msg['args']
        tabs.props(f'model-value={name}')
        panels.props(f'model-value={name}')

    with ui.header().classes(replace='row items-center') as header:
        ui.button(on_click=lambda: left_drawer.toggle()).props('flat color=white icon=menu')

    with ui.element('q-tabs').on('update:model-value', switch_tab) as tabs:
        for name in tab_names:
            ui.element('q-tab').props(f'name={name} label={name}')

    with ui.footer(value=False) as footer:
        ui.label('Footer')

    with ui.left_drawer().classes('bg-blue-100') as left_drawer:
        ui.label('Side menu')

    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        ui.button(on_click=footer.toggle).props('fab icon=contact_support')

    # the page content consists of multiple tab panels
    with ui.element('q-tab-panels').props('model-value=A animated').classes('w-full') as panels:
        for name in tab_names:
            with ui.element('q-tab-panel').props(f'name={name}').classes('w-full'):
                ui.label(f'Content of {name}')
