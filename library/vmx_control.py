#!/usr/bin/python
#
### 'vmx_control' Ansible module ##############################################
#  2016 - Brian LaShomb <brian.lashomb@target.com>
#
### 'vserv' by Joseph Chilcote: https://github.com/chilcote/vserv #############
#  Copyright 2015 Joseph Chilcote
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License. You may obtain a copy
#  of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
##############################################################################

DOCUMENTATION = '''
---
module: vmx_control
short_description: Starts, stops or resets a VM. Can return IP of a VM as an Ansible fact.
'''
EXAMPLES = '''
  - name: Starting the VM and getting IP address
    vmx_control:
      vmx_path="/Users/Shared/output/edge_00163e1e52d91.vmwarevm/edge_00163e1e52d91.vmx"
      vm_mode="started"
      delay_after_firstboot=360
      get_ip=True
'''
RETURN = '''
vm_ip:
    description: IP address of VM
    returned: success
    type: string
    sample: "8.8.8.8"
'''

import os
import subprocess
import time
import shutil

class VMXControl(object):
    '''Operate upon a VMX file'''

    def __init__(self, vmrun = '/Applications/VMware Fusion.app/Contents/Library/vmrun'):
        self.vmrun = vmrun

    def start_vm(self, vmx):
        cmd = [self.vmrun, 'start', vmx]
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = task.communicate()
        if err:
            module.fail_json(msg='Could not process:\t%s' % vmx)

    def stop_vm(self, vmx):
        cmd = [self.vmrun, 'stop', vmx]
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = task.communicate()
        if err:
            module.fail_json(msg='Could not process:\t%s' % vmx)

    def reset_vm(self, vmx):
        cmd = [self.vmrun, 'reset', vmx]
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = task.communicate()
        if err:
            module.fail_json(msg='Could not process:\t%s' % vmx)

    def delete_vm(self, vmx):
        if os.path.exists(os.path.dirname(vmx)):
            shutil.rmtree(os.path.dirname(vmx))

    def get_ip(self, vmx):
        cmd = [self.vmrun, 'getGuestIPAddress', vmx]
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = task.communicate()
        return out.strip()

def main():
    '''Operate upon a VMX file'''
    module = AnsibleModule(
        argument_spec = dict(
            vmx_path=dict(required=True),
            vm_mode=dict(default="started",choices=["started", "stopped", "reset", "deleted"]),
            get_ip=dict(default=True, choices=[True, False], type='bool'),
            delay_after_firstboot=dict(default=False, type='int')
        )
    )
    fusion=VMXControl()
    vmx_path = module.params['vmx_path']
    vm_mode = module.params['vm_mode']
    get_ip = module.params['get_ip']
    delay_after_firstboot = module.params['delay_after_firstboot']

    if vm_mode in "started" and get_ip == True:
        fusion.start_vm(vmx_path)
        time.sleep(delay_after_firstboot)
        module.exit_json(changed=True, ansible_facts=dict(vm_ip=fusion.get_ip(vmx_path)))

    elif vm_mode in "started":
        fusion.start_vm(vmx_path)
        module.exit_json(changed=True)

    elif vm_mode in "stopped":
        fusion.stop_vm(vmx_path)
        module.exit_json(changed=True)

    elif vm_mode in "reset":
        fusion.reset_vm(vmx_path)
        module.exit_json(changed=True)

    elif vm_mode in "deleted":
        fusion.delete_vm(vmx_path)
        module.exit_json(changed=True)


# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
