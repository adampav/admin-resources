from app import app
from flask import render_template
from werkzeug.exceptions import *
import re

from datetime import datetime, timedelta
from flask import jsonify, abort, json, request

query_params = {
    'vms': [],
    'servers': [],
    'network': [],
    'patchpanel': [],
    'devices': [],
}


@app.route('/api/vms', strict_slashes=False)
def get_vms():
    pass


@app.route('/api/vms/<int:vm_id>', strict_slashes=False)
def get_vm(vm_id):
    pass


@app.route('/api/vms/query', strict_slashes=False)
def get_vms_query():
    pass


@app.route('/api/servers', strict_slashes=False)
def get_servers():
    pass


@app.route('/api/servers/<int:server_id>', strict_slashes=False)
def get_server(server_id):
    pass


@app.route('/api/servers/query', strict_slashes=False)
def get_servers_query():
    pass


@app.route('/api/servers/<int:server_id>/vms', strict_slashes=False)
def get_server_vms(server_id):
    pass


@app.route('/api/servers/<int:server_id>/vms/<int:vm_id>', strict_slashes=False)
def get_server_vm(server_id, vm_id):
    pass


@app.route('/api/servers/<int:server_id>/vms/query', strict_slashes=False)
def get_server_vms_query(server_id, vm_id):
    pass


@app.route('/api/networks', strict_slashes=False)
def get_networks():
    pass
    # return jsonify({'episodes': episodes})


@app.route('/api/networks/<int:network_id>', strict_slashes=False)
def get_network(network_id):
    pass
    # return jsonify({'episodes': episodes})


@app.route('/api/networks/query', strict_slashes=False)
def get_networks_query():
    pass
    # return jsonify({'episodes': episodes})


@app.route('/api/patchpanel', strict_slashes=False)
def get_patchpanels():
    pass
    # return jsonify({'episodes': })


@app.route('/api/patchpanel/<int:patchpanel_port>', strict_slashes=False)
def get_patchpanel(patchpanel_port):
    pass
    # return jsonify({'episodes': })


@app.route('/api/patchpanel/query', strict_slashes=False)
def get_patchpanels_query():
    pass
    # return jsonify({'episodes': })


@app.route('/api/devices', strict_slashes=False)
def get_devices():
    try:
        inputJSON = request.json
    except BadRequest, e:
        msg = "ERROR: Invalid JSON"
        return jsonify({'error': msg}), 400


@app.route('/api/devices/<int:device_id>', strict_slashes=False)
def get_device(device_id):
    try:
        inputJSON = request.json
    except BadRequest, e:
        msg = "ERROR: Invalid JSON"
        return jsonify({'error': msg}), 400


@app.route('/api/devices/query', strict_slashes=False)
def get_devices_query():
    try:
        inputJSON = request.json
    except BadRequest, e:
        msg = "ERROR: Invalid JSON"
        return jsonify({'error': msg}), 400

    if inputJSON:
        for val in query_params['devices']:
            if (val in inputJSON) and (type(inputJSON[val]) != unicode):
                return jsonify({'error': 'Bad Request on field %s' % 'showTitle'}), 400

