from app import app
from app import db
from flask_restful import Api, Resource, reqparse, fields, marshal
from werkzeug.exceptions import *
import re
from models import NetDevice, NetDevicePorts, PatchPanel, Network

from datetime import datetime, timedelta
from flask import jsonify, abort, json, request

api = Api(app)

# Params for each model that are expected
query_params = {
    'vms': [],
    'servers': [],
    'network': [],
    'patchpanel': [],
    'netdevices': ['vendor', 'device_type', 'serial_number', 'management_ip'],
    'netdeviceports': ['device_id', 'connected_to', 'vlan', 'ip']
}


class ServerAPI(Resource):
    pass


class ServerListAPI(Resource):
    pass


class VirtualMachineAPI(Resource):
    pass


class VirtualMachineListAPI(Resource):
    pass


class NetworkAPI(Resource):
    pass


class NetworkListAPI(Resource):
    pass


class PatchPanelAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('patch_name', type=str, location='json')
        self.reqparse.add_argument('connected_to', type=str, location='json')
        super(PatchPanelAPI, self).__init__()

    def get(self, patch_id):
        patch = PatchPanel.query.get(patch_id)
        if not patch:
            return {'error': 'No such item'}, 404

        return {'result': patch.serialize}, 200

    def put(self, patch_id):
        patch = PatchPanel.query.get(patch_id)
        if not patch:
            return {'error': 'No such item'}, 404

        args = self.reqparse.parse_args(strict=True)

        for k, v in args.iteritems():
            if v and (patch.__getattribute__(k) != v):
                patch.__setattr__(k, v)

        db.session.commit()

        return {'results': patch.serialize}, 200

    def delete(self, patch_id):
        patch = PatchPanel.query.get(patch_id)
        if not patch:
            return {'error': 'No such item'}, 404

        db.session.delete(patch)
        db.session.commit()

        return {'deleted': patch.serialize}, 200


class PatchPanelListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('description', type=str, location='json', required=True)
        self.reqparse.add_argument('patch_name', type=str, location='json', required=True)
        self.reqparse.add_argument('connected_to', type=str, location='json', required=True)
        super(PatchPanelListAPI, self).__init__()

    def get(self):
        patches = PatchPanel.query.all()
        return {"result": [patch.serialize for patch in patches]}

    def post(self):
        args = self.reqparse.parse_args(strict=True)
        new_patch = PatchPanel()

        for k, v in args.iteritems():
            new_patch.__setattr__(k, v)

        db.session.add(new_patch)
        db.session.commit()

        inserted = PatchPanel.query.order_by('-patch_id').first()

        if not inserted:
            return {'error': 'No such item'}, 404

        return {'results': inserted.serialize}, 200


class NetDevicePortAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('device_id', type=int, location='json')
        self.reqparse.add_argument('connected_to', type=str, location='json')
        self.reqparse.add_argument('vlan', type=int, location='json')
        self.reqparse.add_argument('ip', type=str, location='json')
        super(NetDevicePortAPI, self).__init__()

    def get(self, device_id, port_id):
        device = NetDevice.query.get(device_id)
        if not device:
            return {'error': 'No such item'}, 404

        port = device.device_ports.filter("id=%s" % str(port_id)).first()
        if not port:
            return {'error': 'No such item'}, 404

        return {'result': port.serialize}, 200

    def put(self, device_id, port_id):
        device = NetDevice.query.get(device_id)
        if not device:
            return {'error': 'No such item'}, 404

        port = device.device_ports.filter("id=%s" % str(port_id)).first()
        if not port:
            return {'error': 'No such item'}, 404

        args = self.reqparse.parse_args(strict=True)

        for k, v in args.iteritems():
            if v and (port.__getattribute__(k) != v):
                port.__setattr__(k, v)

        db.session.commit()

        return {'results': port.serialize}, 200

    def delete(self, device_id, port_id):
        device = NetDevice.query.get(device_id)
        if not device:
            return {'error': 'No such item'}, 404

        port = device.device_ports.filter("id=%s" % str(port_id)).first()
        if not port:
            return {'error': 'No such item'}, 404

        db.session.delete(port)
        db.session.commit()

        return {'deleted': port.serialize}, 200


class NetDevicePortListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('device_id', type=int, location='json', required=True)
        self.reqparse.add_argument('connected_to', type=str, location='json', required=True)
        self.reqparse.add_argument('vlan', type=int, location='json', required=True)
        self.reqparse.add_argument('ip', type=str, location='json', required=True)
        super(NetDevicePortListAPI, self).__init__()

    def get(self, device_id):
        device = NetDevice.query.get(device_id)
        if not device:
            return {'error': 'No such item'}, 404

        ports = device.device_ports.all()

        return {'result': [port.serialize for port in ports]}, 200

    def post(self, device_id):
        args = self.reqparse.parse_args(strict=True)
        new_ndp = NetDevicePorts()

        if args['device_id'] != device_id:
            return {'error': 'Incompatible URL and device_id ForeignKey'}, 404

        for k, v in args.iteritems():
            new_ndp.__setattr__(k, v)

        db.session.add(new_ndp)
        db.session.commit()

        inserted = NetDevicePorts.query.order_by('-id').first()

        if not inserted:
            return {'error': 'No such item'}, 404

        return {'results': inserted.serialize}, 200


class NetDeviceAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('vendor', type=str, location='json')
        self.reqparse.add_argument('device_type', type=str, location='json')
        self.reqparse.add_argument('serial_number', type=str, location='json')
        self.reqparse.add_argument('management_ip', type=str, location='json')
        super(NetDeviceAPI, self).__init__()

    def get(self, device_id):
        device = NetDevice.query.get(device_id)
        if not device:
            return {'error': 'No such item'}, 404

        return {'result': device.serialize}, 200

    def put(self, device_id):
        device = NetDevice.query.get(device_id)
        if not device:
            return {'error': 'No such item'}, 404

        args = self.reqparse.parse_args(strict=True)

        for k, v in args.iteritems():
            if v and (device.__getattribute__(k) != v):
                device.__setattr__(k, v)

        db.session.commit()

        return {'results': device.serialize}, 200

    def delete(self, device_id):
        device = NetDevice.query.get(device_id)
        if not device:
            return {'error': 'No such item'}, 404

        db.session.delete(device)
        db.session.commit()

        return {'deleted': device.serialize}, 200


class NetDeviceListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('vendor', type=str, location='json', required=True)
        self.reqparse.add_argument('device_type', type=str, location='json', required=True)
        self.reqparse.add_argument('serial_number', type=str, location='json', required=True)
        self.reqparse.add_argument('management_ip', type=str, location='json', required=True)
        super(NetDeviceListAPI, self).__init__()

    def get(self):
        devices = NetDevice.query.all()
        return {"result": [device.serialize for device in devices]}

    def post(self):
        args = self.reqparse.parse_args(strict=True)
        new_nd = NetDevice()

        for k, v in args.iteritems():
            new_nd.__setattr__(k, v)

        db.session.add(new_nd)
        db.session.commit()

        inserted = NetDevice.query.order_by('-id').first()

        if not inserted:
            return {'error': 'No such item'}, 404

        return {'results': inserted.serialize}, 200

api.add_resource(ServerAPI, '/api/servers/<int:server_id>')
api.add_resource(ServerListAPI, '/api/servers')
api.add_resource(VirtualMachineAPI, '/api/vms/<int:vm_id>')
api.add_resource(VirtualMachineListAPI, '/api/vms')
api.add_resource(NetworkAPI, '/api/networks/<int:network_id>')
api.add_resource(NetworkListAPI, '/api/networks')
api.add_resource(PatchPanelAPI, '/api/patchpanels/<int:patch_id>')
api.add_resource(PatchPanelListAPI, '/api/patchpanels')
api.add_resource(NetDeviceAPI, '/api/netdevices/<int:device_id>')
api.add_resource(NetDeviceListAPI, '/api/netdevices')
api.add_resource(NetDevicePortAPI, '/api/netdevices/<int:device_id>/ports/<int:port_id>')
api.add_resource(NetDevicePortListAPI, '/api/netdevices/<int:device_id>/ports')
