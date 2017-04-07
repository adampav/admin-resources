from app import db


class NetDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor = db.Column(db.String(16))
    device_type = db.Column(db.String(8))
    serial_number = db.Column(db.String(64))
    management_ip = db.Column(db.String(32))
    # device_ports = db.relationship('NetDevicePorts', backref='device', lazy='dynamic')


class NetDevicePorts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('NetDevice.id'))
    connected_to = db.Column(db.String(64))
    vlan = db.Column(db.Integer)
    ip = db.Column(db.String(32))


class IpAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(32))
    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))


class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subnet = db.Column(db.String(24))
    vlan = db.Column(db.Integer)
    addresses = db.relationship('IpAddress', backref='network', lazy='dynamic')
    server_networks = db.relationship('Server', backref='server', lazy='dynamic')
    vm_networks = db.relationship('VM', backref='vm', lazy='dynamic')


class PatchPanel(db.Model):
    patch_id = db.Column(db.String(16), primary_key=True)
    description = db.Column(db.String(64))
    connected_to = db.Column(db.String(64))


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64))
    serial_number = db.Column(db.String(64))
    rack = db.Column(db.String(64))
    unit = db.Column(db.Integer)
    machine_name = db.Column(db.String(64))
    hostname = db.Column(db.String(64))
    vendor = db.Column(db.String(16))
    operating_system = db.Column(db.String(64))
    storage = db.Column(db.String(64))
    ram = db.Column(db.String(64))
    cpu = db.Column(db.String(64))
    network = db.Column(db.String(64))
    server_vms = db.relationship('VM', backref='server', lazy='dynamic')
    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))


class VM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64))
    responsible_person = db.Column(db.String(64))
    machine_name = db.Column(db.String(64))
    hostname = db.Column(db.String(64))
    operating_system = db.Column(db.String(64))
    storage = db.Column(db.String(64))
    ram = db.Column(db.String(64))
    cpu = db.Column(db.String(64))
    network = db.Column(db.String(64))
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
