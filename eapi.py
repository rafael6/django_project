__author__ = 'rafael'

from net_system.models import NetworkDevice
import eapilib
import django
import time


def add_serial_number(target, connection):
    """Use a eapi device and connection object and queries the device for its
     serial number. Stores the serial number in the DB serial_number field."""
    output = connection.run_commands(['show version'])[0]['systemMacAddress']
    target.serial_number = output
    print 'Device: {}   Field: serial_number   Value: {}'\
        .format(target, target.serial_number)


def add_os_version(target, connection):
    """Use a eapi device and connection object and queries the device for its
     os version. Stores the serial number in the DB os_version field."""
    output = connection.run_commands(['show version'])[0]['version']
    target.os_version = output
    print 'Device: {}   Field: os_version   Value: {}'\
        .format(target, target.os_version)


def add_model(target, connection):
    """Use a eapi device and connection object and queries the device for its
     model. Stores the serial number in the DB model field."""
    #print connection.run_commands(['show version'])[0]
    output = connection.run_commands(['show version'])[0]['modelName']
    target.model = output
    print 'Device: {}   Field: model   Value: {}'\
        .format(target, target.model)


def add_uptime(target, connection):
    """Use a eapi device and connection object and queries the device for its
     bootupTiemstamp. Stores the uptime_seconds in the DB serial_number field."""
    raw_output = connection.run_commands(['show version'])[0]['bootupTimestamp']
    time_delta = time.time() - int(raw_output)
    output = int(time_delta)
    target.uptime_seconds = output
    print 'Device: {}   Field: uptime_seconds   Value: {}'\
        .format(target, target.uptime_seconds)


def add_type(target):
    """Stores the device type for a given device."""
    if 'vEOS' in target.model:
        target.device_type = 'SWITCH'
    print 'Device: {}   Field: device_type     Value: {}'\
        .format(target, target.device_type)


def main():
    """Creates a device and a connection objects. Call the appropriate function.
    for database migration and disconnect."""

    django.setup()

    target = NetworkDevice.objects.get(device_name='pynet-sw1')

    eapi_params = {'username': target.credentials.username,
                   'password': target.credentials.password,
                   'port': target.api_port,
                   'hostname': target.ip_address}

    con = eapilib.create_connection(**eapi_params)
    add_serial_number(target, con)
    add_os_version(target, con)
    add_model(target, con)
    add_uptime(target, con)
    add_type(target)


if __name__ == "__main__":
    main()
