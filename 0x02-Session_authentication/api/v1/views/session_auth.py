#!/usr/bin/env python3
""" Session authentication views """
from flask import jsonify, request, abort
from api.v1.app import auth

@app.route('/api/v1/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Handle logout by destroying the session """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
