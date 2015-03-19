__author__ = 'rafael'

from net_system.models import NetworkDevice
from ssh import ssh
import django
import os


def add_serial_number(target, output):
    """Stores the serial number of a given device."""
    target.serial_number = output.strip()
    print 'Device: {}   Field: serial_number   Value: {}'\
        .format(target, target.serial_number)


def add_os_version(target, output):
    """Stores the os version of a given device."""
    os_ver_raw = output.partition("Version ")[2]
    os_ver = os_ver_raw.partition(", ")[0]
    target.os_version = os_ver.strip()
    print 'Device: {}   Field: os_version      Value: {}'\
        .format(target, target.os_version)


def add_model(target, output):
    """Stores the model of a given device."""
    model_raw = output.partition(',')[0]
    model_clean = model_raw.partition('PID: ')[2]
    target.model = model_clean.strip()
    print 'Device: {}   Field: model           Value: {}'\
        .format(target, target.model)


def add_uptime(target, output):
    """Stores the uptime of a given device."""
    lst = output.split(',')
    weeks = int(lst[0].strip(str(target) + 'Uuptime is weeks')) * 604800
    days = int(lst[1].strip('days ')) * 86400
    hours = int(lst[2].strip('hours ')) * 3600
    minutes = int(lst[3].strip('minutes\r\n ')) * 60
    uptime = weeks + days + hours + minutes
    target.uptime_seconds = uptime
    print 'Device: {}   Field: uptime_second   Value: {}'\
        .format(target, target.uptime_seconds)


def add_type(target):
    """Stores the device type for a given device."""
    if '881' in target.model:
        target.device_type = 'ROUTER'
    print 'Device: {}   Field: device_type     Value: {}'\
        .format(target, target.device_type)


def save_config(target, name, output):
    """ Takes a NetworkDevice object, a file name, & the running config (output)
     as arguments. Saves running config to /home/rafael/CFGS with the given file
    name.Stores the file name in db, and print confirmation.
    """
    with open(os.path.join('/home/rafael/CFGS', name), 'w') as f:
        f.write(output)
    target.cfg_file = name
    print 'Device: {}   Field: cfg_file        Value: {}'\
        .format(target, target.cfg_file)


def get_output(target, command):
    """Gets the IP, port, username, and password attributes from a given device.
    Calls SHH function with such attributes and a command to execute. Returns
    the output of the command"""
    output = ssh(target.ip_address, target.ssh_port, target.credentials.username,
                 target.credentials.password, command)
    return output


def main():
    """ Sets django and control script sequence"""
    django.setup()
    target = NetworkDevice.objects.get(device_name='pynet-rtr2')

    serial = get_output(target, 'show snmp chassis')
    add_serial_number(target, serial)

    os = get_output(target, 'sh version | inc Software')
    add_os_version(target, os)

    model = get_output(target, 'show inventory | inc PID')
    add_model(target, model)

    uptime = get_output(target, 'show version | inc uptime')
    add_uptime(target, uptime)

    add_type(target)

    run_config = get_output(target, 'show run')
    save_config(target, str(target) + '_run_config.txt', run_config)


if __name__ == "__main__":
    main()
