from flask import Blueprint

receive = Blueprint('SMS_Receive', __name__)
from . import views
