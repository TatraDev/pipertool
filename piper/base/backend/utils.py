from piper.configurations import get_configuration
from piper.base.rendering import Render

cfg = get_configuration()


def render_fast_api_backend(**kwargs):
    """
    Render backend template to app.py
    """
    fast_api_render = Render('fast-api.j2')
    return fast_api_render.render(**kwargs)


def render_fast_api_tsrct_backend(**kwargs):
    """
    Render backend tesseract template to app.py
    """
    fast_api_tsrct_render = Render('fast-api-tsrct.j2')
    return fast_api_tsrct_render.render(**kwargs)
