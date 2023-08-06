import os
import paramiko
import time
from paramiko.config import SSHConfig

from nerdcore.defs import nl


def _load_ssh_config():
    ssh_config = SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_file):
        with open(user_config_file) as f:
            ssh_config.parse(f)
    return ssh_config


class SSHConnection:
    def __init__(self, server_name):
        self.server_name = server_name
        self.ssh_config = _load_ssh_config()
        self.ssh = self._connect()
        self.shell = None

    def _connect(self):
        cfg = self.ssh_config.lookup(self.server_name)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=cfg['hostname'], username=cfg.get('user'), key_filename=cfg.get('identityfile')[0])
        return ssh

    def execute_command(self, command):
        transport = self.ssh.get_transport()
        transport.set_keepalive(10)
        channel = transport.open_session()
        channel.settimeout(600)  # timeout after 600 seconds
        channel.exec_command(command)

        output = ""
        error_output = ""

        # Buffer the output
        for line in iter(lambda: channel.recv(4096).decode(), ""):
            output += line

        # Buffer the error output
        for line in iter(lambda: channel.recv_stderr(4096).decode(), ""):
            error_output += line

        return output, error_output

    def scp_file_to_server(self, local_path, remote_path):
        sftp = self.ssh.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()

    def scp_file_from_server(self, remote_path, local_path):
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        sftp = self.ssh.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()

    def close(self):
        if self.shell:
            self.shell.close()
        self.ssh.close()
