#!/usr/bin/python
#
### 'create_vmdk' Ansible module ##############################################
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
module: create_vmdk
short_description: Creates a VMDK from a mounted DMG and returns Ansible facts about it.
'''

EXAMPLES = '''
  - name: Creating VMDK image
    create_vmdk:
      disk_id='/dev/disk1'
      output_dir='/Users/Shared/output'
      output_name='edge_00163e1e52d91'
'''
RETURN = '''
disk_type:
    description: Disk type for Fusion (ESXi, etc)
    returned: success
    type: int
    sample: 0
fusion_path:
    description: Path to VMWare Fusion application
    returned: success
    type: string
    sample: "/Applications/VMWare Fusion.app/"
output_dir:
    description: Path to output directory to save VM
    returned: success
    type: string
    sample: "/Users/Shared/output"
output_name:
    description: Name of VM
    returned: success
    type: string
    sample: "edge_00163e1e52d91"
vmpath:
    description: Path to VM
    returned: success
    type: string
    sample: "/Users/Shared/output/edge_00163e1e52d91.vmwarevm"
'''

import os
import subprocess
import plistlib
import shutil


def main():
    '''Converts Base OS DMG to VMDK'''
    module = AnsibleModule(
        argument_spec = dict(
            output_dir=dict(required=False, default=os.getcwd()),
            output_name=dict(required=False, default='osx-vm'),
            disk_id=dict(required=True),
            disk_type=dict(required=False, default=0),
            fusion_path=dict(required=False),
        )
    )
    output_dir = module.params['output_dir']
    output_name = module.params['output_name']
    disk_id = module.params['disk_id']
    disk_type = module.params['disk_type']
    fusion_path = module.params['fusion_path']

    vmpath = os.path.join(output_dir, output_name + '.vmwarevm')
    link = os.path.join(vmpath, os.path.basename(disk_id) + '-link')
    vmdk = os.path.join(vmpath, output_name + '.vmdk')
    if os.path.exists(vmpath):
        module.fail_json(msg='VMware Fusion VM already exists: %s' % vmpath)
    os.mkdir(vmpath)

    if not fusion_path:
        cmd = ['/usr/bin/mdfind', 'kMDItemCFBundleIdentifier == com.vmware.fusion']
        fusion_path = sorted(subprocess.check_output(cmd).strip().split('\n'))[0]

    if not fusion_path:
        try:
          fusion_path = glob.glob('/Applications/VMware Fusion*.app')[0]
        except IndexError:
          module.fail_json(msg='Error: VMware Fusion.app not found')

    fusion_tools_path = os.path.join(fusion_path, 'Contents/Library')

    try:
        cmd = [os.path.join(fusion_tools_path, 'vmware-rawdiskCreator'), 'create', disk_id, 'fullDevice', link, 'lsilogic']
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = task.communicate()
        if err:
            module.fail_json(msg='Error: %s. There is a problem with your DMG, please re-create it and try again' % err.strip())
        cmd = [os.path.join(fusion_tools_path, 'vmware-vdiskmanager'),'-r', link + '.vmdk', '-t', str(disk_type), vmdk]
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = task.communicate()
        if task.returncode:
            if not err:
                module.fail_json(msg='Undetermined error with vmware-vdiskmanager')
    except OSError as e:
        err = 'Failed to execute %s: %s' % (cmd[0], e)
        shutil.rmtree(vmpath)
        module.fail_json(msg='Error: %s' % err)

    os.remove(link + '.vmdk')
    module.exit_json(changed=True, ansible_facts=dict(vmpath=vmpath, output_dir=output_dir, output_name=output_name, disk_type=disk_type, fusion_path=fusion_path))


# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *

main()
