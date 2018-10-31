from .theme import Theme

def setup(app):
    theme = Theme(app)
    app.register_theme('BCGOVTheme', theme.register, theme.apply)
