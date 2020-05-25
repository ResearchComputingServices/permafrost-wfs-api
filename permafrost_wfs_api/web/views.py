#
# Main entry point for all views.
# @version 1.0
# @author Sergiu Buhatel <sergiu.buhatel@carleton.ca>
#

from flask import request, jsonify, url_for, Blueprint
from flask import json, jsonify, Response, blueprints
from permafrost_wfs_api.web.common_view import permafrost_wfs_bp
from permafrost_wfs_api.decorators.crossorigin import crossdomain
from permafrost_wfs_api.decorators.authorization import authorization
import permafrost_wfs_api.web.wfs_view

@permafrost_wfs_bp.route("/", methods=['GET'])
@crossdomain(origin='*')
@authorization
def hello():
    return "Hello World!"

