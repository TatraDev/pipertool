import jinja2
import os


def render_fast_api_backend(**kwargs):
    """
    Render backend template to app.py
    """
    print(os.path.dirname(__file__))
    template_dir = os.path.join(os.path.dirname(__file__), 'templates/')
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                   trim_blocks=True,
                                   lstrip_blocks=True)
    print(jinja_env.list_templates())
    template = jinja_env.get_template('fast-api.j2')
    return template.render(**kwargs)
