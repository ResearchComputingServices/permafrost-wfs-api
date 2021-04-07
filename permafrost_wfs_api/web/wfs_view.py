#
# Specific view. In this case is WFS.
# @version 1.0
# @author Sergiu Buhatel <sergiu.buhatel@carleton.ca>
#

from flask import request, jsonify, url_for, Blueprint
from flask import json, jsonify, Response, blueprints
from permafrost_wfs_api.web.common_view import permafrost_wfs_bp
from permafrost_wfs_api.decorators.crossorigin import crossdomain
from permafrost_wfs_api.decorators.authorization import authorization
import permafrost_wfs_api.web.wfs_view
from owslib.wfs import WebFeatureService
from owslib.fes import *
from owslib.etree import etree
import requests
import re

wfs_server_url = 'http://206.12.92.138/geoserver/pfrost/wms'
wfs_version = '2.0.0'

@permafrost_wfs_bp.route("/identification_title")
@crossdomain(origin='*')
@authorization
def get_identification_title():
    wfs = WebFeatureService(url=wfs_server_url, version=wfs_version)
    return jsonify(results=wfs.identification.title)

@permafrost_wfs_bp.route("/operations")
@crossdomain(origin='*')
@authorization
def get_operations():
    wfs = WebFeatureService(url=wfs_server_url, version=wfs_version)
    results = [operation.name for operation in wfs.operations]
    return jsonify(results=results)

@permafrost_wfs_bp.route("/contents")
@crossdomain(origin='*')
@authorization
def get_contents():
    wfs = WebFeatureService(url=wfs_server_url, version=wfs_version)
    results = list(wfs.contents)
    return jsonify(results=results)

@permafrost_wfs_bp.route("/observations")
@crossdomain(origin='*')
@authorization
def get_observations():
    name_pattern = request.args.get('name_pattern')
    r = requests.get(wfs_server_url + '?service=wfs&version=' + wfs_version + '&request=GetFeature&typeNames=pfrost:locations&outputformat=json')
    result = []
    if r.json():
        items = r.json().get('features')
        items = items if items != None else []
        for item in items:
            new_item = {}
            new_item['lat'] = item.get('geometry').get('coordinates')[1]
            new_item['lng'] = item.get('geometry').get('coordinates')[0]
            new_item['name'] = item.get('properties').get('name')
            new_item['text'] = item.get('properties').get('name')
            new_item['elevation_in_metres'] = item.get('properties').get('elevation_in_metres')
            new_item['comment'] = item.get('properties').get('comment')
            new_item['record_observations'] = item.get('properties').get('record_observations')
            new_item['accuracy_in_metres'] = item.get('properties').get('accuracy_in_metres')
            new_item['provider'] = 'Compute Canada WFS'

            if name_pattern != None:
                search_for = "^" + name_pattern.replace("*", ".*") + "$"
                if re.search(search_for, new_item['name']):
                    result.append(new_item)
            else:
                result.append(new_item)

    return jsonify(result)

