#!/usr/bin/python
#
### 'unmount_dmg' Ansible module ##############################################
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
module: unmount_dmg
short_description: Unmounts a DMG in OS X.
'''
EXAMPLES = '''
  - name: Unmounting source DMG
    unmount_dmg:
      disk_id="/dev/disk1"
'''

import subprocess

def main():
    '''Unmounts Base OS DMG'''
    module = AnsibleModule(
        argument_spec = dict(
            disk_id=dict(required=True)
        )
    )
    disk_id = module.params['disk_id']
    task = subprocess.Popen(['/usr/bin/hdiutil', 'detach', '-force', disk_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = task.communicate()
    module.exit_json(changed=True)
    if err:
        module.fail_json(msg='Could not detach:\t%s' % disk_id)

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *

main()
