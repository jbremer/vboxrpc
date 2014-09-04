from flask import jsonify, request
from flask.ext.classy import FlaskView, route

from lib.vbox import VirtualBox

vb = VirtualBox()

class ApiView(FlaskView):
    @route('/listvms')
    def listvms(self):
        return jsonify(success=True, vms=vb.listvms())

    @route('/revert/<string:vmname>')
    def revert_current(self, vmname):
        vb.revert(vmname, None)
        return jsonify(success=True)

    @route('/revert/<string:vmname>/<string:snapshot>')
    def revert(self, vmname, snapshot):
        vb.revert(vmname, snapshot)
        return jsonify(success=True)

    @route('/startvm/<string:vmname>')
    def startvm(self, vmname):
        vb.startvm(vmname)
        return jsonify(success=True)

    @route('/status/<string:vmname>')
    def status(self, vmname):
        return jsonify(success=True, status=vb.status(vmname))

    @route('/stopvm/<string:vmname>')
    def stopvm(self, vmname):
        # TODO Add forced killing of VirtualBox instances in case this command
        # gives an error.
        vb.stopvm(vmname)
        return jsonify(success=True)

    @route('/createvm/<string:vmname>')
    def createvm(self, vmname):
        vb.createvm(vmname)
        return jsonify(success=True)

    @route('/deletevm/<string:vmname>')
    def deletevm(self, vmname):
        vb.deletevm(vmname)
        return jsonify(success=True)

    @route('/ramsize/<string:vmname>/<int:ramsize>')
    def ramsize(self, vmname, ramsize):
        vb.ramsize(vmname, ramsize)
        return jsonify(success=True)

    @route('/os-type/<string:vmname>/<string:ostype>')
    def ostype(self, vmname, ostype):
        vb.os_type(vmname, ostype)
        return jsonify(success=True)

    @route('/create-hdd/<string:vmname>/<int:disksize>')
    def createhdd(self, vmname, disksize):
        vb.create_hdd(vmname, disksize)
        return jsonify(success=True)

    @route('/attach-iso/<string:vmname>/<string:filename>')
    def attachiso(self, vmname, filename):
        vb.attach_iso(vmname, filename)
        return jsonify(success=True)

    @route('/detach-iso/<string:vmname>')
    def detachiso(self, vmname):
        vb.detach_iso(vmname)
        return jsonify(success=True)

    @route('/extra-data/<string:vmname>')
    def extradata(self, vmname):
        vb.extra_data(vmname, request.args.get('key'),
                      request.args.get('value'))
        return jsonify(success=True)

    @route('/mac-address/<string:vmname>/<string:adapter>/<string:mac>')
    def macaddress(self, vmname, adapter, mac):
        vb.mac_address(vmname, adapter, mac)
        return jsonify(success=True)

    @route('/push-iso/<string:filename>', methods=['POST'])
    def pushiso(self, filename):
        f = request.files['file']
        if f:
            vb.push_iso(f, filename)
        return jsonify(success=True)

    @route('/hwvirt/<string:vmname>/<int:enable>')
    def hwvirt(self, vmname, enable):
        vb.hwvirt(vmname, bool(enable))
        return jsonify(success=True)

    @route('/snapshot/<string:vmname>/<string:label>')
    def snapshot(self, vmname, label):
        vb.snapshot(vmname, label, request.args.get('description', ''))
        return jsonify(success=True)

    @route('/nic/<string:vmname>/<string:key>/<string:value>')
    def nic(self, vmname, key, value):
        vb.nic(vmname, key, value)
        return jsonify(success=True)

    @route('/hostonlyifs')
    def hostonlyifs(self):
        return jsonify(success=True, content=vb.hostonlyifs())
