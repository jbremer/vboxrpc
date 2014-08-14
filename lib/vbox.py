import logging
import subprocess


VBoxManage = '/usr/bin/VBoxManage'
log = logging.getLogger(__name__)


class VirtualBox(object):
    def __init__(self, vboxmanage=None):
        self.vboxmanage = vboxmanage or VBoxManage

    def _call(self, *args, **kwargs):
        cmd = [self.vboxmanage] + list(args)

        for k, v in kwargs.items():
            if v is None or v is True:
                cmd += ['--' + k]
            else:
                cmd += ['--' + k, str(v)]

        try:
            ret = subprocess.check_output(cmd)
        except subprocess.CalledProcessError as e:
            log.error('Error running command: %s', e)
            return None

        return ret.strip()

    def listvms(self):
        ret = []

        for line in self._call('list', 'vms').split('\n'):
            ret.append(line.split('"')[1])

        return ret

    def revert(self, vmname, snapshot):
        if not snapshot:
            return self._call('snapshot', vmname, 'restorecurrent')
        else:
            return self._call('snapshot', vmname, 'restore', snapshot)

    def startvm(self, vmname):
        return self._call('startvm', vmname, type='headless')

    def status(self, vmname):
        ret = {}

        buf = self._call('showvminfo', vmname, machinereadable=True)
        for line in buf.split('\n'):
            key, value = line.split('=', 1)

            if value[0] == '"' and value[-1] == '"':
                value = value[1:-1]

            ret[key.strip()] = value.strip()

        return ret

    def stopvm(self, vmname):
        return self._call('controlvm', vmname, 'poweroff')
