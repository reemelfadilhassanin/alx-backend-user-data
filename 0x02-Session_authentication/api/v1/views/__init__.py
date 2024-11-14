#!/usr/bin/env python3
""" Initialize the API views """

from api.v1.views.session_auth import *  # Import session_auth at the top
from flask import Blueprint

# Define the app_views Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Other view imports can go here
# from api.v1.views.some_other_view import *
