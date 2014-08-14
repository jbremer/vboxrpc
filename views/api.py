from flask import jsonify
from flask.ext.classy import FlaskView, route

from lib.vbox import VirtualBox

vb = VirtualBox()

class ApiView(FlaskView):
    @route('/listvms/')
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

    @route('/stopvm/<string:vmname>')
    def stopvm(self, vmname):
        vb.stopvm(vmname)
        return jsonify(success=True)
