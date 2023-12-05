from flask import Blueprint, render_template

you=Blueprint('you', __name__, url_prefix='/you')

from . import views