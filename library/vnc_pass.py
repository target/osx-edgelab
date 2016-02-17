#!/usr/bin/python
#
### 'vnc_pass' Ansible module ################################################
#  2016 - Brian LaShomb <brian.lashomb@target.com>
##############################################################################

DOCUMENTATION = '''
---
module: vnc_pass
short_description: Generates a random password of specified length.
'''
EXAMPLES = '''
  - name: Generating a random password
    passwd_length: 20
'''
RETURN = '''
vnc_pass:
    description: Random password
    returned: success
    type: string
    sample: "cL5LNnM4XaRg31HHAKDf"
'''

import string
import random
def main():
    '''Generate random password'''
    module = AnsibleModule(
        argument_spec = dict(
            passwd_length=dict(required=False, default=20, type='int')
        )
    )
    passwd_length = module.params['passwd_length']

    # Just alphanumeric characters
    chars = string.letters + string.digits
    module.exit_json(changed=True, ansible_facts=dict(vnc_pass=''.join((random.choice(chars)) for x in range(passwd_length))))

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *

main()
