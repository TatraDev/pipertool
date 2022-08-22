import jinja2
import os


def render_fast_api_backend(**kwargs):
    """
    Render backend template to app.py
    """
    template = get_backend_template('fast-api.j2')
    return template.render(**kwargs)


def render_fast_api_tsrct_backend(**kwargs):
    """
    Render backend tesseract template to app.py
    """
    template = get_backend_template('fast-api-tsrct.j2')
    return template.render(**kwargs)


def get_backend_template(template_fn):
    """
    Returns template data for j2 file
    """
    template_dir = os.path.join(os.path.dirname(__file__), 'templates/')
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = jinja_env.get_template(template_fn)
    return template