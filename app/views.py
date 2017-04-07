from app import app
from app import db
from flask import render_template
from werkzeug.exceptions import *
import re
from models import NetDevice

from datetime import datetime, timedelta
from flask import jsonify, abort, json, request

query_params = {
    'vms': [],
    'servers': [],
    'network': [],
    'patchpanel': [],
    'netdevices': ['vendor', 'device_type', 'serial_number', "management_ip"],
}

model_params = {
    'vms': [],
    'servers': [],
    'network': [],
    'patchpanel': [],
    'netdevices': ['id','vendor', 'device_type', 'serial_number', "management_ip"],
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
        for device in devices:
            dc = {}
            for param in model_params['netdevices']:
                dc[param] = device.__getattribute__(param)
            results.append(dc)

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
            # TODO perform the checks for all fields
            new = NetDevice()
            for param in query_params['netdevices']:
                if (param in input_json) and (type(input_json[param]) != unicode):
                    return jsonify({'error': 'Bad Request on field %s' % param}), 400
                elif param not in input_json:
                    return jsonify({'error': 'Bad JSON field %s is needed' % param}), 400
                else:
                    new.__setattr__(param, input_json[param])
            print new.device_type
            db.session.add(new)
            db.session.commit()
            return jsonify({'result': input_json})
        #
        #     print new
        # #     if 'episodeTitle' in inputJSON:
        #         episodes = [episode for episode in episodes
        #                     if re.search(inputJSON['episodeTitle'], episode['episodeTitle'], re.IGNORECASE)]
        #
        #     if 'idShow' in inputJSON:
        #         episodes = [episode for episode in episodes if episode['idShow'] == int(inputJSON['idShow'])]
        #
        #     if 'season' in inputJSON:
        #         episodes = [episode for episode in episodes if episode['season'] == int(inputJSON['season'])]
        #
        #     if 'episode' in inputJSON:
        #         episodes = [episode for episode in episodes if episode['episode'] == int(inputJSON['episode'])]
        #
        #     if 'dateReleased' in inputJSON:
        #         a = datetime.strptime(inputJSON['dateReleased'], "%Y-%m-%d")
        #         episodes = [episode for episode in episodes if episode['dateReleased'] and
        #                     a < datetime.strptime(episode['dateReleased'], "%Y-%m-%d %H:%M:%S")]
        #
        #     if 'dateAdded' in inputJSON:
        #         a = datetime.strptime(inputJSON['dateAdded'], "%Y-%m-%d")
        #         episodes = [episode for episode in episodes if episode['dateAdded'] and
        #                     a < datetime.strptime(episode['dateAdded'], "%Y-%m-%d %H:%M:%S")]
        #
        #     if 'lastPlayed' in inputJSON:
        #         a = datetime.strptime(inputJSON['lastPlayed'], "%Y-%m-%d")
        #         episodes = [episode for episode in episodes if episode['lastPlayed'] and
        #                     a < datetime.strptime(episode['lastPlayed'], "%Y-%m-%d %H:%M:%S")]
        #
        # if len(episodes) == 0:
        #     jsonify({'msg': 'No Results found'})
        #
        # return jsonify({'episodes': episodes})




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

