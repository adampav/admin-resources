from app import db


class NetDevice(db.Model):
    __tablename__ = 'NetDevice'
    id = db.Column(db.Integer, primary_key=True)
    vendor = db.Column(db.String(16))
    device_type = db.Column(db.String(8))
    serial_number = db.Column(db.String(64))
    management_ip = db.Column(db.String(32))
    device_ports = db.relationship('NetDevicePorts', backref='device', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'vendor': self.vendor,
            'device_type': self.device_type,
            'serial_number': self.serial_number,
            'management_ip': self.management_ip,
        }


class NetDevicePorts(db.Model):
    __tablename__ = 'NetDevicePorts'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('NetDevice.id'))
    connected_to = db.Column(db.String(64))
    vlan = db.Column(db.Integer)
    ip = db.Column(db.String(32))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'connected_to': self.connected_to,
            'vlan': self.vlan,
            'ip': self.ip,
        }


class IpAddress(db.Model):
    __tablename__ = 'IpAddress'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(32))
    network_id = db.Column(db.Integer, db.ForeignKey('Network.id'))
    hostname = db.Column(db.String(64))
    # TODO add IpAddress type from sqlalchemy_utils

    @property
    def serialize(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'hostname': self.hostname,
            'network_id': self.network_id,
        }


class Network(db.Model):
    __tablename__ = 'Network'
    id = db.Column(db.Integer, primary_key=True)
    subnet = db.Column(db.String(24))
    vlan = db.Column(db.Integer)
    ip_networks = db.relationship('IpAddress', backref='network_ip', lazy='dynamic')
    server_networks = db.relationship('Server', backref='network_server', lazy='dynamic')
    vm_networks = db.relationship('VirtualMachine', backref='network_vms', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'subnet': self.subnet,
            'vlan': self.vlan,
        }


class PatchPanel(db.Model):
    __tablename__ = 'PatchPanel'
    patch_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64))
    patch_name = db.Column(db.String(64))
    connected_to = db.Column(db.String(64))

    @property
    def serialize(self):
        return {
            'patch_id': self.patch_id,
            'description': self.description,
            'patch_name': self.patch_name,
            'connected_to': self.connected_to,
        }


class Server(db.Model):
    __tablename__ = 'Server'
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
    server_vms = db.relationship('VirtualMachine', backref='server', lazy='dynamic')
    network_id = db.Column(db.Integer, db.ForeignKey('Network.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'serial_number': self.serial_number,
            'rack': self.rack,
            'unit': self.unit,
            'machine_name': self.machine_name,
            'hostname': self.hostname,
            'vendor': self.vendor,
            'operating_system': self.operating_system,
            'storage': self.storage,
            'ram': self.ram,
            'cpu': self.cpu,
        }


class VirtualMachine(db.Model):
    __tablename__ = 'VirtualMachine'
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
    server_id = db.Column(db.Integer, db.ForeignKey('Server.id'))
    network_id = db.Column(db.Integer, db.ForeignKey('Network.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'responsible_person': self.responsible_person,
            'machine_name': self.machine_name,
            'hostname': self.hostname,
            'operating_system': self.operating_system,
            'storage': self.storage,
            'ram': self.ram,
            'cpu': self.cpu,
            'server_id': self.server_id,
        }
