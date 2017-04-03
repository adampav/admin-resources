from app import db


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor = db.Column(db.String(16))
    serial_number = db.Column(db.String(64))
    management_ip = db.Column(db.String(32))
    device_ports = db.relationship('DevicePorts', backref='device', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.nickname


class DevicePorts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    connected_to = db.Column(db.String(64))
    vlan = db.Column(db.Integer)
    ip = db.Column(db.String(32))


class IpAddress(db.model):
    pass


class Network(db.Model):
    pass


class PatchPanel(db.Model):
    patch_id = db.Column(db.String(16), primary_key=True)
    description = db.Column(db.String(64))
    connected_to = db.Column(db.String(64))


class Server(db.model):
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


class VM(db.model):
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