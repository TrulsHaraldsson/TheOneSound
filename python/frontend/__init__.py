import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates'),
        extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_'],
        autoescape=True)