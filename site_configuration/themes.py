from flask import current_app
from flaskext.themes import get_theme, render_theme_template

def get_current_theme():
    theme = current_app.config.get("THEME", "plain")
    return get_theme(theme)

def render(template, **context):
    return render_theme_template(get_current_theme(), template, **context)
