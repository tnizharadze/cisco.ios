#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_l2vpn
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_l2vpn
short_description: Resource module to configure L2VPN.
description:
  - This module provides declarative management of Layer 2 VPN on Cisco IOS
  - network devices.
version_added: 1.0.0
author: Timur Nizharadze (@tnizharadze)
notes:
  - Tested against Cisco IOS XE Version 17.10.01prd7 on CML.
options:
  config:
    description: The provided configurations.
    type: dict
    suboptions:
      l2vpn:
        description: Base L2 VPN configurations.
        type: dict
        suboptions:
          logging:
            description: Default Logging configuretion.
            type: dict
            suboptions:
              pseudowire_status:
                description: Enable L2VPN Pseudowire logging
                type: bool
              redundancy:
                description: To enable system message log (syslog) reporting of the status redundancy group
                type: bool
              vc_state:
                description: Enable EVPN-VPWS for logging
                type: bool
          redundancy_predictive_enabled:
            description: Configuring Predictive Switchover
            type: bool
          pseudowire_group_status:
            description: Sends pseudowire group status messages.
            type: bool
          router_id:
            description: Set global router-id
            type: str
          shutdown:
            description: Disable all L2VPN
            type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
    type: str
  state:
    description:
      - The state the configuration should be left in
      - The states I(rendered), I(gathered) and I(parsed) does not perform any change
        on the device.
      - The state I(rendered) will transform the configuration in C(config) option to
        platform specific CLI commands which will be returned in the I(rendered) key
        within the result. For state I(rendered) active connection to remote host is
        not required.
      - The state I(gathered) will fetch the running configuration from device and transform
        it into structured data in the format as per the resource module argspec and
        the value is returned in the I(gathered) key within the result.
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into JSON format as per the resource module parameters and the
        value is returned in the I(parsed) key within the result. The value of C(running_config)
        option should be the same format as the output of command I(show running-config
        | section ^l2vpn$) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
    choices:
    - merged
    - replaced
    - deleted
    - rendered
    - parsed
    - gathered
    default: merged
"""

EXAMPLES = """

"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: list
  sample:
    - l2vpn
    - logging pseudowire status
    - router-id 4.4.4.4
    - shutdown
    - exit
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - l2vpn
    - logging pseudowire status
    - router-id 4.4.4.4
    - shutdown
    - exit
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when I(state) is C(parsed)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.l2vpn.l2vpn import (
    L2vpnArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.l2vpn.l2vpn import (
    L2vpn,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=L2vpnArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = L2vpn(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
