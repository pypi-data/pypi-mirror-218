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
        stdin, stdout, stderr = self.ssh.exec_command(command)

        while not stdout.channel.exit_status_ready():
            # Wait for the command to complete
            time.sleep(1)

        output = stdout.read().decode()
        error_output = stderr.read().decode()

        return output, error_output

    def scp_file_to_server(self, local_path, remote_path):
        sftp = self.ssh.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()

    def scp_file_from_server(self, remote_path, local_path):
        sftp = self.ssh.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()

    def close(self):
        if self.shell:
            self.shell.close()
        self.ssh.close()
