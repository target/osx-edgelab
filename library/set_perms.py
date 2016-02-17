#!/usr/bin/python
#
### 'set_perms' Ansible module ###############################################
#  2016 - Brian LaShomb <brian.lashomb@target.com>
##############################################################################

DOCUMENTATION = '''
---
module: set_perms
short_description: Changes permissions so we are able to operate on the VM.
'''
EXAMPLES = '''
  - name: Setting permissions for the new VMDK image
    set_perms:
      path="/Users/Shared/output/edge_00163e1e52d91.vmwarevm"
      user="admin"
      group="admin"
'''

import subprocess

def main():
    '''Sets the permissions of given path to specified user'''
    module = AnsibleModule(
        argument_spec = dict(
            path=dict(required=True, type='str'),
            user=dict(required=True, type='str'),
            group=dict(required=False, default='staff', type='str')
        )
    )
    path = module.params['path']
    user = module.params['user']
    group = module.params['group']
    subprocess.call(['chown', '-R', user, ':', group, path])
    subprocess.call(['chmod', '-R', '777', path])
    module.exit_json(changed=True)

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *

main()
