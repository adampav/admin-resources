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


class IpAddress(db.Model):
    __tablename__ = 'IpAddress'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(32))
    network_id = db.Column(db.Integer, db.ForeignKey('Network.id'))


class Network(db.Model):
    __tablename__ = 'Network'
    id = db.Column(db.Integer, primary_key=True)
    subnet = db.Column(db.String(24))
    vlan = db.Column(db.Integer)
    ip_networks = db.relationship('IpAddress', backref='network_ip', lazy='dynamic')
    server_networks = db.relationship('Server', backref='network_server', lazy='dynamic')
    vm_networks = db.relationship('VirtualMachine', backref='network_vms', lazy='dynamic')


class PatchPanel(db.Model):
    __tablename__ = 'PatchPanel'
    patch_id = db.Column(db.String(16), primary_key=True)
    description = db.Column(db.String(64))
    connected_to = db.Column(db.String(64))


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
