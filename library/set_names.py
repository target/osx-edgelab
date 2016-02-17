#!/usr/bin/python
#
### 'set_names' Ansible module ###############################################
#  2016 - Brian LaShomb <brian.lashomb@target.com>
##############################################################################

DOCUMENTATION = '''
---
module: set_names
short_description: Sets the ComputerName, HostName and LocalHostName for the VM.
'''
EXAMPLES = '''
  - name: Setting names for VM
    set_names:
      vm_name="edge_00163e1e52d91"
'''

import subprocess

def main():
    '''Sets the names of the VM'''
    module = AnsibleModule(
        argument_spec = dict(
            vm_name=dict(required=True, type='str')
        )
    )
    vm_name = module.params['vm_name']
    subprocess.Popen(['scutil', '--set', 'ComputerName', vm_name])
    subprocess.Popen(['scutil', '--set', 'HostName', vm_name])
    subprocess.Popen(['scutil', '--set', 'LocalHostName', vm_name])
    module.exit_json(changed=True)

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *

main()
