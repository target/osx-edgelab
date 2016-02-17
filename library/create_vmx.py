#!/usr/bin/python
#
### 'create_vmx' Ansible module ###############################################
#  2016 - Brian LaShomb <brian.lashomb@target.com>
#
### 'vfuse' by Joseph Chilcote: https://github.com/chilcote/vfuse #############
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
module: create_vmx
short_description: Creates a valid VMX file and returns the path to it.
'''
EXAMPLES = '''
  - name: Creating a valid VMX file
    create_vmx:
      vmpath="/Users/Shared/output/edge_00163e1e52d91.vmwarevm"
      output_name="edge_00163e1e52d91"
      mem_size=4096
      connection_type="bridged"
'''
RETURN = '''
vmx:
    description: Path to VMX file
    returned: success
    type: string
    sample: "/Users/Shared/output/edge_00163e1e52d91.vmwarevm/edge_00163e1e52d91.vmx"
'''

import os

def main():
    '''Generates a working VMX file'''
    module = AnsibleModule(
        argument_spec = dict(
            vmpath=dict(required=True),
            output_name=dict(required=True),
            guest_os=dict(required=False),
            hw_version=dict(required=False, default=12, choices=[8, 9, 10, 11, 12], type='int'),
            mem_size=dict(required=False, default=2048, type='int'),
            connection_type=dict(required=False, default='bridged'),
            enable3d=dict(required=False),
            vnc_port=dict(required=False),
            vnc_passwd=dict(required=False),
            mac_address=dict(required=False),
            hw_model=dict(required=False),
            serial_number=dict(required=False),
            serial_format=dict(required=False),
            shared_folder=dict(required=False)
        )
    )
    vmpath = module.params['vmpath']
    output_name = module.params['output_name']
    guest_os = module.params['guest_os']
    hw_version = module.params['hw_version']
    mem_size = module.params['mem_size']
    connection_type = module.params['connection_type']
    enable3d = module.params['enable3d']
    vnc_port = module.params['vnc_port']
    vnc_passwd = module.params['vnc_passwd']
    mac_address = module.params['mac_address']
    hw_model = module.params['hw_model']
    serial_number = module.params['serial_number']
    serial_format = module.params['serial_format']
    shared_folder = module.params['shared_folder']

    vmx = os.path.join(vmpath, output_name + '.vmx')
    guest_os = 'darwin%d-64' % (hw_version + 3)

    with open(vmx, 'w') as f:
        f.write('.encoding = "UTF-8"\n')
        f.write('config.version = "8"\n')
        f.write('virtualhw.version = "%d"\n' % hw_version)
        f.write('numvcpus = "2"\n')
        f.write('sata0.present = "TRUE"\n')
        f.write('memsize = "%d"\n' % mem_size)
        f.write('sata0:0.present = "TRUE"\n')
        f.write('sata0:0.fileName = "%s.vmdk"\n' % output_name)
        f.write('sata0:1.present = "TRUE"\n')
        f.write('sata0:1.autodetect = "TRUE"\n')
        f.write('sata0:1.deviceType = "cdrom-raw"\n')
        f.write('sata0:1.startConnected = "FALSE"\n')
        f.write('ethernet0.present = "TRUE"\n')
        f.write('ethernet0.connectionType = "%s"\n' % connection_type)
        f.write('ethernet0.virtualDev = "e1000e"\n')
        f.write('ethernet0.wakeOnPcktRcv = "FALSE"\n')
        f.write('ethernet0.linkStatePropagation.enable = "TRUE"\n')
        f.write('usb.present = "TRUE"\n')
        f.write('ehci.present = "TRUE"\n')
        f.write('ehci.pciSlotNumber = "0"\n')
        f.write('pciBridge0.present = "TRUE"\n')
        f.write('pciBridge4.present = "TRUE"\n')
        f.write('pciBridge4.virtualDev = "pcieRootPort"\n')
        f.write('pciBridge4.functions = "8"\n')
        f.write('pciBridge5.present = "TRUE"\n')
        f.write('pciBridge5.virtualDev = "pcieRootPort"\n')
        f.write('pciBridge5.functions = "8"\n')
        f.write('pciBridge6.present = "TRUE"\n')
        f.write('pciBridge6.virtualDev = "pcieRootPort"\n')
        f.write('pciBridge6.functions = "8"\n')
        f.write('pciBridge7.present = "TRUE"\n')
        f.write('pciBridge7.virtualDev = "pcieRootPort"\n')
        f.write('pciBridge7.functions = "8"\n')
        f.write('vmci0.present = "TRUE"\n')
        f.write('smc.present = "TRUE"\n')
        f.write('hpet0.present = "TRUE"\n')
        f.write('ich7m.present = "TRUE"\n')
        f.write('firmware = "efi"\n')
        f.write('displayname = "%s"\n' % output_name)
        f.write('guestos = "%s"\n' % guest_os)
        f.write('nvram = "%s.nvram"\n' % output_name)
        f.write('keyboardAndMouseProfile = "macProfile"\n')
        f.write('floppy0.present = "FALSE"\n')
        f.write('msg.autoanswer = "TRUE"')
        if enable3d:
            f.write('\nmks.enable3d = "TRUE"')
        else:
            f.write('\nmks.enable3d = "FALSE"')
        if vnc_passwd:
            f.write('\nremotedisplay.vnc.enabled = "TRUE"\n')
            f.write('remotedisplay.vnc.port = "%s"\n' % vnc_port)
            f.write('RemoteDisplay.vnc.key = "%s"' % vnc_passwd)
        if mac_address:
            f.write('\nethernet0.addressType = "static"\n')
            f.write('ethernet0.address = "%s"' % mac_address)
        else:
            f.write('\nethernet0.addressType = "generated"')
        if hw_model:
            f.write('\nhw.model = "%s"' % hw_model)
        if serial_number:
            f.write('\nserialNumber = "%s"' % serial_number)
        if serial_format:
            f.write('\nSMBIOS.use12CharSerialNumber = "TRUE"')
        if shared_folder:
            f.write('\nsharedFolder0.present = "true"\n')
            f.write('sharedFolder0.enabled = "true"\n')
            f.write('sharedFolder0.readAccess = "true"\n')
            f.write('sharedFolder0.writeAccess = "true"\n')
            f.write('sharedFolder0.hostPath = "%s"\n' % shared_folder)
            f.write('sharedFolder0.guestName = "-vfuse"\n')
            f.write('sharedFolder0.expiration = "never"\n')
            f.write('sharedfolder.maxnum = "1"')
    module.exit_json(changed=True, ansible_facts=dict(vmx=vmx))


# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *

main()
