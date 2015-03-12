__author__ = 'rafael'

import paramiko
import socket


def ssh(ip, port, username, password, command):
    """Open and SSH channel with the given parameters, execute a given command
     on the remote system and returns the command output."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, port, username, password,
                       look_for_keys=False, allow_agent=False)
    except socket.error:
        return 'Node %s is not answering; check hostname or IP.' % ip
    except paramiko.AuthenticationException:
        return 'Authentication failed; check username and password.'
    except KeyboardInterrupt:
        print '  Goodbye'
        exit()
    else:
        stdin, stdout, stderr = client.exec_command(command)
        return stdout.read()
    finally:
        client.close()
        
        
if __name__ == "__main__":
    ssh()
