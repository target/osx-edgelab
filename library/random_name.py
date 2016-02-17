#!/usr/bin/python
#
### 'random_name' Ansible module #############################################
#  2016 - Brian LaShomb <brian.lashomb@target.com>
##############################################################################

DOCUMENTATION = '''
---
module: random_name
short_description: Generates a random MAC Address and/or modifed for use a VM Name.
'''
EXAMPLES = '''
  - name: Generating random name for VM
    random_name: generate_name=True
'''
RETURN = '''
vm_name:
    description: Name of new VM
    returned: success
    type: string
    sample: "edge_00163e1e52d91"
'''

import random

def randomMAC():
    return [ 0x00, 0x16, 0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]

def MACprettyprint(mac):
    return ''.join(map(lambda x: "%02x" % x, mac))

def main():
    '''Generates random MAC address and removes the colons'''
    module = AnsibleModule(
        argument_spec = dict(
            generate_name=dict(default=True, choices=[True, False], type='bool'),
            generate_MAC=dict(default=False, choices=[True, False], type='bool')
        )
    )
    generate_name = module.params['generate_name']
    generate_MAC = module.params['generate_MAC']
    if generate_name == True and generate_MAC == True:
        module.exit_json(changed=True, ansible_facts=dict(vm_name="edge_" + MACprettyprint(randomMAC()), mac_addr=(randomMAC())))
    elif generate_name == True:
        module.exit_json(changed=True, ansible_facts=dict(vm_name="edge_" + MACprettyprint(randomMAC())))
    elif generate_MAC == True:
        module.exit_json(changed=True, ansible_facts=dict(mac_addr=(randomMAC())))

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *

main()
