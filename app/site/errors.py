from flask import render_template
from .import site

@site.app_errorhandler(404)
def page_not_found(e):
    return render_template('site/404.html'), 404

@site.app_errorhandler(500)
def internal_server_error(e):
    return render_template('site/500.html'), 500
