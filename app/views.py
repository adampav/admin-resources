from app import app
from app import db
from flask_restful import Api, Resource, reqparse
import re
from models import NetDevice, NetDevicePorts, PatchPanel, Network, IpAddress, VirtualMachine, Server

api = Api(app)


class VirtualMachineAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('ip', type=str, location='json')
        self.reqparse.add_argument('network_id', type=int, location='json')
        super(VirtualMachineAPI, self).__init__()

    def get(self, server_id, vm_id):
        server = Server.query.get(server_id)
        if not server:
            return {'error': 'No such item'}, 404

        vm = server.server_vms.filter("id=%s" % str(vm_id)).first()

        if not vm:
            return {'error': 'No such item'}, 404

        return {'result': {'vm': vm.serialize, 'server': server.serialize}}, 200

    def put(self, server_id, vm_id):
        server = Server.query.get(server_id)
        if not server:
            return {'error': 'No such item'}, 404

        vm = server.ip_networks.filter("id=%s" % str(vm_id)).first()

        if not vm:
            return {'error': 'No such item'}, 404

        args = self.reqparse.parse_args(strict=True)

        for k, v in args.iteritems():
            if v and (vm.__getattribute__(k) != v):
                vm.__setattr__(k, v)

        db.session.commit()

        return {'result': {'vm': vm.serialize, 'server': server.serialize}}, 200

    def delete(self, server_id, vm_id):
        server = Server.query.get(server_id)
        if not server:
            return {'error': 'No such item'}, 404

        vm = server.ip_networks.filter("id=%s" % str(vm_id)).first()

        if not vm:
            return {'error': 'No such item'}, 404

        db.session.delete(server)
        db.session.commit()

        return {'result': {'vm': vm.serialize, 'server': server.serialize}}, 200


class VirtualMachineListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('vm', type=str, location='json', required=True)
        self.reqparse.add_argument('network_id', type=int, location='json', required=True)
        super(VirtualMachineListAPI, self).__init__()

    def get(self, server_id):
        server = Server.query.get(server_id)
        if not server:
            return {'error': 'No such item'}, 404

        vms = server.ip_networks.all()

        return {"result": {'vms': [vm.serialize for vm in vms], 'server': server.serialize}}

    def post(self, server_id):
        args = self.reqparse.parse_args(strict=True)
        new_vm = VirtualMachine()

        if args['server_id'] != server_id:
            return {'error': 'Incompatible URL and server_id ForeignKey'}, 404

        for k, v in args.iteritems():
            new_vm.__setattr__(k, v)

        db.session.add(new_vm)
        db.session.commit()

        inserted = VirtualMachine.query.order_by('-id').first()

        if not inserted:
            return {'error': 'No such item'}, 404

        return {'results': inserted.serialize}, 200


class ServerAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('subnet', type=str, location='json')
        self.reqparse.add_argument('vlan', type=int, location='json')
        super(ServerAPI, self).__init__()

    def get(self, server_id):
        server = Server.query.get(server_id)
        if not server:
            return {'error': 'No such item'}, 404

        return {'result': server.serialize}, 200

    def put(self, server_id):
        server = Server.query.get(server_id)
        if not server:
            return {'error': 'No such item'}, 404

        args = self.reqparse.parse_args(strict=True)

        for k, v in args.iteritems():
            if v and (server.__getattribute__(k) != v):
                server.__setattr__(k, v)

        db.session.commit()

        return {'results': server.serialize}, 200

    def delete(self, server_id):
        server = Server.query.get(server_id)
        if not server:
            return {'error': 'No such item'}, 404

        db.session.delete(server)
        db.session.commit()

        return {'deleted': server.serialize}, 200


class ServerListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('subnet', type=str, location='json', required=True)
        self.reqparse.add_argument('vlan', type=int, location='json', required=True)
        super(ServerListAPI, self).__init__()

    def get(self):
        servers = Server.query.all()
        return {"result": [server.serialize for server in servers]}

    def post(self):
        args = self.reqparse.parse_args(strict=True)
        new_server = Server()

        for k, v in args.iteritems():
            new_server.__setattr__(k, v)

        db.session.add(new_server)
        db.session.commit()

        inserted = Server.query.order_by('-id').first()

        if not inserted:
            return {'error': 'No such item'}, 404

        return {'results': inserted.serialize}, 200


class IpAddressAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('ip', type=str, location='json')
        self.reqparse.add_argument('network_id', type=int, location='json')
        super(IpAddressAPI, self).__init__()

    def get(self, network_id, address_id):
        network = Network.query.get(network_id)
        if not network:
            return {'error': 'No such item'}, 404

        ip = network.ip_networks.filter("id=%s" % str(address_id)).first()

        if not ip:
            return {'error': 'No such item'}, 404

        return {'result': {'ip': ip.serialize, 'network': network.serialize}}, 200

    def put(self, network_id, address_id):
        network = Network.query.get(network_id)
        if not network:
            return {'error': 'No such item'}, 404

        ip = network.ip_networks.filter("id=%s" % str(address_id)).first()

        if not ip:
            return {'error': 'No such item'}, 404

        args = self.reqparse.parse_args(strict=True)

        for k, v in args.iteritems():
            if v and (ip.__getattribute__(k) != v):
                ip.__setattr__(k, v)

        db.session.commit()

        return {'results': ip.serialize}, 200

    def delete(self, network_id, address_id):
        network = Network.query.get(network_id)
        if not network:
            return {'error': 'No such item'}, 404

        ip = network.ip_networks.filter("id=%s" % str(address_id)).first()

        if not ip:
            return {'error': 'No such item'}, 404

        db.session.delete(network)
        db.session.commit()

        return {'result': {'ip': ip.serialize, 'network': network.serialize}}, 200


class IpAddressListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('ip', type=str, location='json', required=True)
        self.reqparse.add_argument('network_id', type=int, location='json', required=True)
        super(IpAddressListAPI, self).__init__()

    def get(self, network_id):
        network = Network.query.get(network_id)
        if not network:
            return {'error': 'No such item'}, 404

        ips = network.ip_networks.all()

        return {"result": {'ips': [ip.serialize for ip in ips], 'network': network.serialize}}

    def post(self, network_id):
        args = self.reqparse.parse_args(strict=True)
        new_ip = IpAddress()

        if args['network_id'] != network_id:
            return {'error': 'Incompatible URL and network_id ForeignKey'}, 404

        for k, v in args.iteritems():
            new_ip.__setattr__(k, v)

        db.session.add(new_ip)
        db.session.commit()

        inserted = IpAddress.query.order_by('-id').first()

        if not inserted:
            return {'error': 'No such item'}, 404

        return {'results': inserted.serialize}, 200


class NetworkAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('subnet', type=str, location='json')
        self.reqparse.add_argument('vlan', type=int, location='json')
        super(NetworkAPI, self).__init__()

    def get(self, network_id):
        network = Network.query.get(network_id)
        if not network:
            return {'error': 'No such item'}, 404

        return {'result': network.serialize}, 200

    def put(self, network_id):
        network = Network.query.get(network_id)
        if not network:
            return {'error': 'No such item'}, 404

        args = self.reqparse.parse_args(strict=True)

        for k, v in args.iteritems():
            if v and (network.__getattribute__(k) != v):
                network.__setattr__(k, v)

        db.session.commit()

        return {'results': network.serialize}, 200

    def delete(self, network_id):
        network = Network.query.get(network_id)
        if not network:
            return {'error': 'No such item'}, 404

        db.session.delete(network)
        db.session.commit()

        return {'deleted': network.serialize}, 200


class NetworkListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('subnet', type=str, location='json', required=True)
        self.reqparse.add_argument('vlan', type=int, location='json', required=True)
        super(NetworkListAPI, self).__init__()

    def get(self):
        networks = Network.query.all()
        return {"result": [network.serialize for network in networks]}

    def post(self):
        args = self.reqparse.parse_args(strict=True)
        new_network = Network()

        for k, v in args.iteritems():
            new_network.__setattr__(k, v)

        db.session.add(new_network)
        db.session.commit()

        inserted = Network.query.order_by('-id').first()

        if not inserted:
            return {'error': 'No such item'}, 404

        return {'results': inserted.serialize}, 200


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
api.add_resource(VirtualMachineAPI, '/api/servers/<int:server_id>/vms/<int:vm_id>')
api.add_resource(VirtualMachineListAPI, '/api/servers/<int:server_id>/vms')
api.add_resource(IpAddressAPI, '/api/networks/<int:network_id>/ips/<int:address_id>')
api.add_resource(IpAddressListAPI, '/api/networks/<int:network_id>/ips')
api.add_resource(NetworkAPI, '/api/networks/<int:network_id>')
api.add_resource(NetworkListAPI, '/api/networks')
api.add_resource(PatchPanelAPI, '/api/patchpanels/<int:patch_id>')
api.add_resource(PatchPanelListAPI, '/api/patchpanels')
api.add_resource(NetDeviceAPI, '/api/netdevices/<int:device_id>')
api.add_resource(NetDeviceListAPI, '/api/netdevices')
api.add_resource(NetDevicePortAPI, '/api/netdevices/<int:device_id>/ports/<int:port_id>')
api.add_resource(NetDevicePortListAPI, '/api/netdevices/<int:device_id>/ports')
