#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_vlan_configuration
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_vlan_configuration
short_description: Resource module to configure vlans
description:
  - This module provides declarative management of vlan configuration on Cisco IOS
  - network devices.
version_added: 1.0.0
author: Timur Nizharadze (@tnizharadze)
notes:
  - Tested against Cisco IOS XE Version 17.10.01prd7 on CML.
options:
  config:
    description: VLAN configuration
    type: list
    elements: dict
    suboptions:
      vlan:
        description:
          - "VLAN ID List Eg. 1-10,15"
          - "Caution: for EVPN configuration use only one VLAN"
        type: str
        required: true
      member:
        description: Member configuration
        type: dict
        mutually_exclusive: [["vfi", "access_vfi"], ["vni", "evpn"], [vfi", "evpn"]]
        suboptions:
          vfi:
            description: Virtual Forwarding Instance (VFI) member name
            type: str
          access_vfi:
            description: Access VFI as Member of the VLAN of a Border VTEP
            type: str
          vni:
            description: VxLan vni
            type: str
          ip_peer:
            description: L2VPN peers configuration
            type: list
            elements: dict
            required_together: [["address", "vc_id"]]
            suboptions:
              address:
                description: IP address of the peer
                type: str
              vc_id:
                description: VC ID value
                type: str
              template:
                description: Template to use for encapsulation and protocol configuration
                type: str
          pseudowire:
            description: L2VPN peers configuration
            type: list
            elements: dict
            required_together: [["address", "vc_id"]]
            suboptions:
              pwnumber:
                description: <1-100000> Pseudowire interface number
                type: str
              address:
                description: IP address of the peer
                type: str
              vc_id:
                description: VC ID value
                type: str
              template:
                description: Template to use for encapsulation and protocol configuration
                type: str
          evpn:
            description: Ethernet Virtual Private Network (EVPN)
            type: dict
            required_together: [["instance", "vni"]]
            suboptions:
              instance:
                description: <1-65535>  EVPN instance
                type: str
                required: true
              vni:
                description: <4096-16777215>  VxLAN VNI value
                type: str
              protected:
                description: Enable local peer to peer blocking
                type: bool
                default: false
      mdns_sd_gateway:
        description: Enable mDNS config on vlan/interface
        type: dict
        suboptions:
          enable:
            description: Enable mDNS gateway on vlan/interface
            type: bool
            required: true
          active_query_timer:
            description: mDNS Active Query Timer value
            type: str
          transport:
            description: mDNS message processing on a specific transport
            type: str
            choices: ["ipv4","ipv6","both"]
          service_inst_suffix:
            description: Suffix String (MAX 10 Characters) to append while exporting Service
            type: str
          service_mdns_query:
            description: mDNS Query request message processing
            type: str
            choices: ["ptr","all"]
          source_interface:
            description: Configure source interface to communicate with SDG Agent
            type: str
          sdg_agent:
            description: Configure sdg-agent IPv4 address
            type: str
          service_policy:
            description: mDNS service policy
            type: str
      et_analytics_enable:
        description: Enable et-analytics on VLAN
        type: bool
      device_tracking:
        description: Configure device-tracking on the vlan
        type: dict
        required_by: {"attach_policy": "enable"}
        suboptions:
          enable:
            description: Enable device tracking
            type: bool
          attach_policy:
            description: Policy name for device-tracking
            type: str
      ipv6:
        description: ipv6 root chain
        type: dict
        suboptions:
          destination_guard:
            description: Configure destination guard on the vlan
            type: dict
            required_by: {"attach_policy": "enable"}
            suboptions:
              enable:
                description: Enable destination guard on the vlan
                type: bool
              attach_policy:
                description: Apply a policy for feature Destination Guard
                type: str
          dhcp:
            description: IPv6 dhcp configuration commands
            type: dict
            suboptions:
              guard:
                description: Configure IPv6 DHCP guard on the vlan
                type: dict
                required_by: {"attach_policy": "enable"}
                suboptions:
                  enable:
                    description: Enable IPv6 DHCP guard on the vlan
                    type: bool
                  attach_policy:
                    description: Apply a policy for feature IPv6 DHCP guard
                    type: str
              ldra_attach_policy:
                description: Configure IPv6 DHCP LDRA on the vlan
                type: str
                choices: ["client-facing-trusted","client-facing-untrusted"]
          nd:
            description: IPv6 Neighbour Discovery configuration commands
            type: dict
            suboptions:
              ra_throttler:
                description: Configure RA throttler on the vlan
                type: dict
                required_by: {"attach_policy": "enable"}
                suboptions:
                  enable:
                    description: Enable RA throttler on the vlan
                    type: bool
                  attach_policy:
                    description: Apply a policy for feature RA throttler
                    type: str
              raguard:
                description: Configure ipv6 raguard on the vlan
                type: dict
                required_by: {"attach_policy": "enable"}
                suboptions:
                  enable:
                    description: Enable ipv6 raguard on the vlan
                    type: bool
                  attach_policy:
                    description: Apply a policy for feature raguard
                    type: str
              suppress:
                description: Configure ND suppress on the vlan
                type: dict
                required_by: {"attach_policy": "enable"}
                suboptions:
                  enable:
                    description: Enable ND suppress on the vlan
                    type: bool
                  attach_policy:
                    description: Apply a policy for feature ND suppress
                    type: str
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
        | section ^vlan configuration) executed on device. For state I(parsed) active
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
    - sample command 1
    - sample command 2
    - sample command 3
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - sample command 1
    - sample command 2
    - sample command 3
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vlan_configuration.vlan_configuration import (
    Vlan_configurationArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.vlan_configuration.vlan_configuration import (
    Vlan_configuration,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Vlan_configurationArgs.argument_spec,
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

    result = Vlan_configuration(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
