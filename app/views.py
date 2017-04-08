from app import app
from app import db
from flask import render_template
from werkzeug.exceptions import *
import re
from models import NetDevice, NetDevicePorts

from datetime import datetime, timedelta
from flask import jsonify, abort, json, request

# Params for each model that are expected
query_params = {
    'vms': [],
    'servers': [],
    'network': [],
    'patchpanel': [],
    'netdevices': ['vendor', 'device_type', 'serial_number', 'management_ip'],
    'netdeviceports': ['device_id', 'connected_to', 'vlan', 'ip']
}

# All model values returned
model_params = {
    'vms': [],
    'servers': [],
    'network': [],
    'patchpanel': [],
    'netdevices': ['id', 'vendor', 'device_type', 'serial_number', 'management_ip'],
    'netdeviceports': ['id', 'device_id', 'connected_to', 'vlan', 'ip']
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


@app.route('/api/netdevices', strict_slashes=False, methods=['GET', 'POST'])
def get_netdevices():
    if request.method == 'GET':
        devices = NetDevice.query.all()
        results = []

        return jsonify({"result": [device.serialize for device in devices]})

    if request.method == 'POST':

        # Validate JSON
        try:
            input_json = request.json
        except BadRequest, e:
            msg = "ERROR: Invalid JSON"
            return jsonify({'error': msg}), 400

        # return jsonify({"result": input_json})

        # Check JSON fields

        if input_json:
            # TODO perform the checks for all fields
            new_nd = NetDevice()
            for param in query_params['netdevices']:
                if (param in input_json) and (type(input_json[param]) != unicode):
                    return jsonify({'error': 'Bad Request on field %s' % param}), 400
                elif param not in input_json:
                    return jsonify({'error': 'Bad JSON field %s is needed' % param}), 400
                else:
                    new_nd.__setattr__(param, input_json[param])

            db.session.add(new_nd)
            db.session.commit()
            return jsonify({'result': input_json})


@app.route('/api/netdevices/<int:device_id>', strict_slashes=False)
def get_netdevice(device_id):
    try:
        inputJSON = request.json
    except BadRequest, e:
        msg = "ERROR: Invalid JSON"
        return jsonify({'error': msg}), 400


@app.route('/api/netdevices/query', strict_slashes=False)
def get_netdevices_query():
    try:
        inputJSON = request.json
    except BadRequest, e:
        msg = "ERROR: Invalid JSON"
        return jsonify({'error': msg}), 400

    if inputJSON:
        for val in query_params['devices']:
            if (val in inputJSON) and (type(inputJSON[val]) != unicode):
                return jsonify({'error': 'Bad Request on field %s' % 'showTitle'}), 400


@app.route('/api/netdevices/<int:device_id>/ports', strict_slashes=False, methods=['GET', 'POST'])
def get_netdevice_ports(device_id):
    if request.method == 'GET':
        device = NetDevice.query.get(device_id)

        if not device:
            abort(404)

        device_ports = device.device_ports.all()

        results = []

        for dport in device_ports:
            dp = {}
            for param in model_params['netdeviceports']:
                dp[param] = dport.__getattribute__(param)
            results.append(dp)

        return jsonify({"result": results})

    if request.method == 'POST':
        # Validate JSON
        try:
            input_json = request.json
        except BadRequest, e:
            msg = "ERROR: Invalid JSON"
            return jsonify({'error': msg}), 400

        # return jsonify({"result": input_json})

        # Check JSON fields
        if input_json:
            new_nd_ports = NetDevicePorts()
            if 'device_id' not in input_json or (input_json['device_id'] != str(device_id)):
                return jsonify({'error': 'Bad JSON Field %s not present or not matching with URL' % 'device_id'}), 400

            for param in query_params['netdeviceports']:
                if (param in input_json) and (type(input_json[param]) != unicode):
                    return jsonify({'error': 'Bad Request on field %s' % param}), 400
                elif param not in input_json:
                    return jsonify({'error': 'Bad JSON field %s is needed' % param}), 400
                else:
                    new_nd_ports.__setattr__(param, input_json[param])

            db.session.add(new_nd_ports)
            db.session.commit()

            inserted = NetDevicePorts.query.order_by('-id').first()
            results = {}
            for param in model_params['netdeviceports']:
                results[param] = inserted.__getattribute__(param)

            return jsonify({"result": results})

        return jsonify({'error': "no JSON"}), 400
