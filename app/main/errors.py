from flask import template_rendered
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return template_rendered('404.html'),404

@main.app_errorhandler(500)
def internal_server_error(e):
    return template_rendered('500.html'),500