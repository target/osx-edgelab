#!/usr/bin/python
#
### 'mount_dmg' Ansible module ################################################
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
module: mount_dmg
short_description: Mounts a DMG in OS X and returns the disk id as an Ansible fact.
'''
EXAMPLES = '''
  - name: Mounting source DMG
    mount_dmg:
      source_dmg="/Users/Shared/input/elcap_base.dmg"
'''
RETURN = '''
disk_id:
    description: Disk ID of mounted DMG
    returned: success
    type: string
    sample: "/dev/disk1"
'''

import subprocess
import plistlib

def main():
    '''Mounts base DMG'''
    module = AnsibleModule(
        argument_spec = dict(
            source_dmg=dict(required=True)
        )
    )
    source_dmg = module.params['source_dmg']
    d = {}
    try:
        output = subprocess.check_output(['/usr/bin/hdiutil', 'attach', '-nobrowse', '-noverify', '-noautoopen', source_dmg, '-plist'])
        d = plistlib.readPlistFromString(output)
        for i in d['system-entities']:
            if 'mount-point' in str(i):
                mount_point = i['mount-point']
                mountpoint_dev_entry = i['dev-entry']
            if 'GUID_partition_scheme' in str(i):
                disk_id = i['dev-entry']
        if not disk_id:
            module.fail_json(msg='Warning: your DMG does not have a partition scheme, and vfuse may fail')
            disk_id = mountpoint_dev_entry
        module.exit_json(changed=True, ansible_facts=dict(disk_id=disk_id))
    except subprocess.CalledProcessError as err:
        module.fail_json(msg='Cannot mount dmg: %s' % source_dmg)

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *

main()
