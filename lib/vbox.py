import logging
import os.path
import subprocess

from lib.config import config


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

    def attach_iso(self, vmname, filename):
        isopath = os.path.join(config('iso-dir'), os.path.basename(filename))

        ctlname = 'IDE Controller'
        self._call('storageattach', vmname, storagectl=ctlname,
                   type='dvddrive', port=1, device=0, medium=isopath)

    def create_hdd(self, vmname, disksize):
        hddpath = os.path.join(config('hdd-dir'),
                               '%s.iso' % os.path.basename(vmname))

        ctlname = 'IDE Controller'
        self._call('createhd', filename=hddpath, size=disksize)
        self._call('storagectl', vmname, name=ctlname, add='ide')
        self._call('storageattach', vmname, storagectl=ctlname,
                   type='hdd', device=0, port=0, medium=hddpath)

    def createvm(self, vmname):
        self._call('createvm', name=vmname, basefolder=config('vms-dir'),
                   register=True)

    def detach_iso(self, vmname):
        ctlname = 'IDE Controller'
        self._call('storageattach', vmname, storagectl=ctlname,
                   type='dvddrive', port=1, device=0, medium='emptydrive')

    def extra_data(self, vmname, key, value):
        return self._call('setextradata', vmname, key, value)

    def hostonlyifs(self):
        return self._call('list', 'hostonlyifs')

    def listvms(self):
        ret = []

        for line in self._call('list', 'vms').split('\n'):
            ret.append(line.split('"')[1])

        return ret

    def mac_address(self, vmname, adapter, mac):
        return self._call('modifyvm', vmname, **{adapter: mac})

    def nic(self, vmname, key, value):
        return self._call('modifyvm', vmname, **{key: value})

    def os_type(self, vmname, ostype):
        operating_systems = {
            'xp': 'WindowsXP',
        }
        return self._call('modifyvm', vmname,
                          ostype=operating_systems[ostype])

    def push_iso(self, f):
        isopath = os.path.join(config('iso-dir'),
                               os.path.basename(f.filename))
        f.save(isopath)

    def ramsize(self, vmname, ramsize):
        return self._call('modifyvm', vmname, memory=ramsize)

    def revert(self, vmname, snapshot):
        if not snapshot:
            return self._call('snapshot', vmname, 'restorecurrent')
        else:
            return self._call('snapshot', vmname, 'restore', snapshot)

    def snapshot(self, vmname, label, description):
        return self._call('snapshot', vmname, 'take', label,
                          description=description, live=True)

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
