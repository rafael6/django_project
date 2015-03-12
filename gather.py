__author__ = 'rafael'

from net_system.models import NetworkDevice
from ssh import ssh
import django


def get_serial_number(target, command):
    """Gets the IP, port, username, and password attributes from a given device.
    Calls SHH function with such attributes and parses the command output for a
    serial number."""
    output = ssh(target.ip_address, target.ssh_port, target.credentials.username,
                 target.credentials.password, command)
    target.serial_number = output.strip()
    print 'Stored serial number {} on serial_number field for device {}.'\
        .format(target.serial_number, target)


def get_os_version(target, command):
    """Gets the IP, port, username, and password attributes from a given device.
    Calls SHH function with such attributes and parses the command output for
    the OS version."""
    output = ssh(target.ip_address, target.ssh_port, target.credentials.username,
                 target.credentials.password, command)
    os_ver_raw = output.partition("Version ")[2]
    os_ver = os_ver_raw.partition(", ")[0]
    target.os_version = os_ver.strip()
    print 'Stored OS version {} on os_version field for device {}.'\
        .format(target.os_version, target)


def get_model(target, command):
    """Gets the IP, port, username, and password attributes from a given device.
    Calls SHH function with such attributes and parses the command output for
    the serial number."""
    output = ssh(target.ip_address, target.ssh_port, target.credentials.username,
                 target.credentials.password, command)
    model_raw = output.partition(',')[0]
    model_clean = model_raw.partition('PID: ')[2]
    target.model = model_clean.strip()
    print 'Stored model number {} on the model field for device {}.'\
        .format(target.model, target)


def get_uptime(target, command):
    """Gets the IP, port, username, and password attributes from a given device.
    Calls SHH function with such attributes and parses the command output for
    the uptime."""
    output = ssh(target.ip_address, target.ssh_port, target.credentials.username,
                 target.credentials.password, command)
    output_normalize = output.split("is ")[1]
    weeks_raw = output_normalize.partition("weeks")[0]
    weeks = int(weeks_raw) * 604800
    days_raw = output_normalize.partition("days")[0]
    days = int(days_raw.partition(", ")[2].strip()) * 86400
    hours_raw = output_normalize.partition("hours")[0]
    hours = int(hours_raw.partition("days, ")[2].strip()) * 3600
    mins_raw = output_normalize.partition("hours, ")[2]
    mins = int(mins_raw.partition(" minutes")[0].strip()) * 60
    uptime = weeks + days + hours + mins
    target.uptime_seconds = uptime
    print 'Stored uptime {} on the uptime field for device {}.'\
        .format(target.uptime_seconds, target)


def main():
    """ Sets django and control script sequence"""
    django.setup()
    target = NetworkDevice.objects.get(device_name='pynet-rtr2')
    get_serial_number(target, 'show snmp chassis')
    get_os_version(target, 'sh ver | inc Software')
    get_model(target, 'show inventory | inc PID')
    get_uptime(target, 'show version | inc uptime')


if __name__ == "__main__":
    main()
    
