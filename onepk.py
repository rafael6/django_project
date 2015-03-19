__author__ = 'rafael'

import django
import onepk_helper
from net_system.models import NetworkDevice


def connect(ip, username, password, pin, port):
    """Use an ip, username, password, pin-file, & port as parameters to create
    a onep device object. Establishes a session & returns the device object"""
    device = onepk_helper.NetworkDevice(ip, username, password, pin, port)
    device.establish_session()
    return device


def add_serial_number(target, connection):
    """Use a onep device and connection object and queries the device for its
     serial number. Stores the serial number in the DB serial_number field."""
    target.serial_number = connection.net_element.properties.SerialNo
    print 'Device: {}   Field: serial_number   Value: {}'\
        .format(target, target.serial_number)


def add_os_version(target, connection):
    """Use a onep device and connection object and queries the device for its
     system description. Removes the os version from the command output and
     stores the sos version in the DB os_version field."""
    description = connection.net_element.properties.sys_descr
    os = description.split(', ')[2].strip('Version ')
    target.os_version = os
    print 'Device: {}   Field: os_version      Value: {}'\
        .format(target, target.os_version)


def add_model(target, connection):
    """Use a onep device and connection object and queries the device for its
     product id. Stores the product id in the DB model field."""
    target.model = connection.net_element.properties.product_id
    print 'Device: {}   Field: model           Value: {}'\
        .format(target, target.model)


def add_uptime(target, connection):
    """Use a onep device and connection object and queries the device for its
     system uptime. Stores the system uptime in the DB uptime_seconds field."""
    target.uptime_seconds = connection.net_element.properties.sys_uptime
    print 'Device: {}   Field: uptime_second   Value: {}'\
        .format(target, target.uptime_seconds)


def add_type(target):
    """Stores the device type for a given device."""
    if '881' in target.model:
        target.device_type = 'ROUTER'
    print 'Device: {}   Field: device_type     Value: {}'\
        .format(target, target.device_type)


def disconnect(device):
    """Use a device object and disconnects its onep session"""
    device.disconnect()


def main():
    """Creates a device and a connection objects. Call the appropriate function.
    for database migration and disconnect."""
    django.setup()
    target = NetworkDevice.objects.get(device_name='pynet-rtr1')
    con = connect(target.ip_address, target.credentials.username,
                  target.credentials.password, 'pynet-rtr1-pin.txt', target.api_port)
    add_serial_number(target, con)
    add_os_version(target, con)
    add_model(target, con)
    add_uptime(target, con)
    add_type(target)
    disconnect(con)


if __name__ == "__main__":
    main()
