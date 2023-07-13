#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_l2vpn_evpn
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_l2vpn_evpn
short_description: Resource module to configure L2VPN EVPN default settings.
description:
  - This module provides declarative management of L2VPN EVPN default settings on Cisco IOS
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
      logging:
        description: Configure logging flags
        type: dict
        suboptions:
          peer_state:
            description: Configure EVPN peer logging
            type: bool
          vpws_vc_state:
            description: Configure EVPN VPWS logging flags
            type: bool
      replication_type:
        description: Specify method for replicating BUM traffic
        type: str
        choices: ["static", "ingress"]
      flooding_suppression_address_resolution_disable:
        description:
          - Disable flooding suppression of  Address Resolution and Neighbor
          - Discovery Protocol packets. Equivalent of IOS command
        type: bool
      ip_duplication:
        description: IP duplication detection
        type: dict
        required_together: [["limit", "time"]]
        suboptions:
          limit:
            description:
              - Number of IP moves within specified time interval.
              - Allowed value between 2-1000.
            type: int
          time:
            description:
              - Time interval, Seconds.
              - Allowed value between 10-36000.
            type: int
      mac_duplication:
        description: MAC duplication detection
        type: dict
        required_together: [["limit", "time"]]
        suboptions:
          limit:
            description:
              - Number of MAC moves within specified time interval
              - <2-1000>
            type: int
          time:
            description:
              - MAC duplication timer
              - <10-36000> Seconds
            type: int
      router_id:
        description: EVPN router ID
        type: str
      multihoming_aliasing_disable:
        description: Multihoming aliasing disable
        type: bool
      ip_local_learning:
        description: IP local learning from dataplane
        type: dict
        suboptions:
          disable:
            description: Disable IP local learning from dataplane
            type: bool
          limit_per_mac_ipv4:
            description:
              - Limit number of IPv4 addresses (default 4)
              - <0-32000>  Maximum number of addresses
            type: int
          limit_per_mac_ipv6:
            description:
              - Limit number of IPv6 addresses (default 12)
              - <0-32000>  Maximum number of addresses
            type: int
          time:
            description: IP local learning timer values
            type: dict
            suboptions:
              down:
                description:
                  - Down time (default 10 minutes)
                  - <1-1440>  Number of minutes
                type: int
              poll:
                description:
                  - Polling interval (default 1 minute)
                  - <1-1440>  Number of minutes
                type: int
              reachable:
                description:
                  - Reachable lifetime (default 5 minutes)
                  - <1-1440>  Number of minutes
                type: int
              stale:
                description:
                  - Stale lifetime (default 30 minutes)
                  - <1-1440>  Number of minutes
                type: int
      default_gateway_advertise:
        description: Advertise Default Gateway MAC/IP routes
        type: bool
      route_target_auto_vni:
        description: Automatically set a vni-based route-target
        type: bool
      multicast_advertise:
        description: Enable and advertise L2 multicast capability
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
        | section ^l2vpn evpn$) executed on device. For state I(parsed) active
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
# Using gathered

# Before state:
# -------------
# l2vpn evpn
#  logging vpws vc-state
#  logging peer state
#  replication-type static
#  flooding-suppression address-resolution disable
#  ip duplication limit 234 time 234
#  mac duplication limit 213 time 123
#  router-id Loopback0
#  multihoming aliasing disable
#  ip local-learning disable
#  ip local-learning limit per-mac ipv4 345
#  ip local-learning limit per-mac ipv6 2345
#  ip local-learning time down 234
#  ip local-learning time poll 223
#  ip local-learning time reachable 234
#  ip local-learning time stale 23
#  default-gateway advertise
#  route-target auto vni
#  multicast advertise

- name: Gather the existing ios_l2vpn_evpn running configuration
  register: result
  cisco.ios.ios_l2vpn_evpn:
    state: gathered

# Task Output:
# ------------
# "gathered": {
#     "default_gateway_advertise": true,
#     "flooding_suppression_address_resolution_disable": true,
#     "ip_duplication": {
#         "limit": 234,
#         "time": 234
#     },
#     "ip_local_learning": {
#         "disable": true,
#         "limit_per_mac_ipv4": 345,
#         "limit_per_mac_ipv6": 2345,
#         "time": {
#             "down": 234,
#             "poll": 223,
#             "reachable": 234,
#             "stale": 23
#         }
#     },
#     "logging": {
#         "peer_state": true,
#         "vpws_vc_state": true
#     },
#     "mac_duplication": {
#         "limit": 213,
#         "time": 123
#     },
#     "multicast_advertise": true,
#     "multihoming_aliasing_disable": true,
#     "replication_type": "static",
#     "route_target_auto_vni": true,
#     "router_id": "Loopback0"
# }

# Using parsed

# Before state:
# -------------
# cat _parsed.cfg
# l2vpn evpn
#  logging vpws vc-state
#  logging peer state
#  replication-type static
#  flooding-suppression address-resolution disable
#  ip duplication limit 234 time 234
#  mac duplication limit 213 time 123
#  router-id Loopback0
#  multihoming aliasing disable
#  ip local-learning disable
#  ip local-learning limit per-mac ipv4 345
#  ip local-learning limit per-mac ipv6 2345
#  ip local-learning time down 234
#  ip local-learning time poll 223
#  ip local-learning time reachable 234
#  ip local-learning time stale 23
#  default-gateway advertise
#  route-target auto vni
#  multicast advertise

- name: Parse the commands for provided configuration
  register: result
  cisco.ios.ios_l2vpn_evpn:
    running_config: "{{ lookup('file', '_parsed.cfg') }}"
    state: parsed

# Task Output:
# ------------
# "parsed": {
#     "default_gateway_advertise": true,
#     "flooding_suppression_address_resolution_disable": true,
#     "ip_duplication": {
#         "limit": 234,
#         "time": 234
#     },
#     "ip_local_learning": {
#         "disable": true,
#         "limit_per_mac_ipv4": 345,
#         "limit_per_mac_ipv6": 2345,
#         "time": {
#             "down": 234,
#             "poll": 223,
#             "reachable": 234,
#             "stale": 23
#         }
#     },
#     "logging": {
#         "peer_state": true,
#         "vpws_vc_state": true
#     },
#     "mac_duplication": {
#         "limit": 213,
#         "time": 123
#     },
#     "multicast_advertise": true,
#     "multihoming_aliasing_disable": true,
#     "replication_type": "static",
#     "route_target_auto_vni": true,
#     "router_id": "Loopback0"
# }

# Using rendered

- name: Render the commands for provided ios_l2vpn_evpn configuration
  register: result
  cisco.ios.ios_l2vpn_evpn:
    config:
      logging:
        peer_state: true
        vpws_vc_state: true
      replication_type: "static"
      flooding_suppression_address_resolution_disable: true
      ip_duplication:
        limit: 234
        time: 234
      mac_duplication:
        limit: 213
        time: 123
      router_id: "Loopback0"
      multihoming_aliasing_disable: true
      ip_local_learning:
        disable: true
        limit_per_mac_ipv4: 345
        limit_per_mac_ipv6: 2345
        time:
          down: 234
          poll: 223
          reachable: 234
          stale: 23
      default_gateway_advertise: true
      route_target_auto_vni: true
      multicast_advertise: true
    state: rendered

# Task Output:
# ------------
# "rendered": [
#     "l2vpn evpn",
#     "logging peer state",
#     "logging vpws vc-state",
#     "replication-type static",
#     "flooding-suppression address-resolution disable",
#     "ip duplication limit 234 time 234",
#     "mac duplication limit 213 time 123",
#     "router-id Loopback0",
#     "multihoming aliasing disable",
#     "ip local-learning disable",
#     "ip local-learning limit per-mac ipv4 345",
#     "ip local-learning limit per-mac ipv6 2345",
#     "ip local-learning time down 234",
#     "ip local-learning time poll 223",
#     "ip local-learning time reachable 234",
#     "ip local-learning time stale 23",
#     "default-gateway advertise",
#     "route-target auto vni",
#     "multicast advertise",
#     "exit"
# ]

# Using merged

# Before state:
# -------------
# l2vpn evpn
#  logging vpws vc-state
#  logging peer state
#  replication-type static
#  flooding-suppression address-resolution disable
#  ip duplication limit 234 time 234
#  mac duplication limit 213 time 123
#  router-id Loopback0
#  multihoming aliasing disable

- name: Merge provided ios_l2vpn_evpn configuration with device configuration
  register: result
  cisco.ios.ios_l2vpn_evpn:
    config:
      logging:
        peer_state: true
        vpws_vc_state: true
      replication_type: "static"
      flooding_suppression_address_resolution_disable: true
      ip_duplication:
        limit: 234
        time: 234
      mac_duplication:
        limit: 213
        time: 123
      router_id: "Loopback0"
      multihoming_aliasing_disable: true
    state: merged

# Task Output:
# ------------
# "commands": [
#     "l2vpn evpn",
#     "ip local-learning disable",
#     "ip local-learning limit per-mac ipv4 345",
#     "ip local-learning limit per-mac ipv6 2345",
#     "ip local-learning time down 234",
#     "ip local-learning time poll 223",
#     "ip local-learning time reachable 234",
#     "ip local-learning time stale 23",
#     "exit"
# ]
#
# After state:
# -------------
# l2vpn evpn
#  logging vpws vc-state
#  logging peer state
#  replication-type static
#  flooding-suppression address-resolution disable
#  ip duplication limit 234 time 234
#  mac duplication limit 213 time 123
#  router-id Loopback0
#  multihoming aliasing disable
#  ip local-learning disable
#  ip local-learning limit per-mac ipv4 345
#  ip local-learning limit per-mac ipv6 2345
#  ip local-learning time down 234
#  ip local-learning time poll 223
#  ip local-learning time reachable 234
#  ip local-learning time stale 23

# Using replaced

# Before state:
# -------------
# l2vpn evpn
#  logging vpws vc-state
#  logging peer state
#  replication-type static
#  flooding-suppression address-resolution disable
#  ip duplication limit 234 time 234
#  mac duplication limit 213 time 123
#  router-id Loopback0
#  multihoming aliasing disable
#  ip local-learning disable
#  ip local-learning limit per-mac ipv4 345
#  ip local-learning limit per-mac ipv6 2345
#  ip local-learning time down 234
#  ip local-learning time poll 223
#  ip local-learning time reachable 234
#  ip local-learning time stale 23
#  default-gateway advertise
#  route-target auto vni
#  multicast advertise

- name: Replace provided l2vpn configuration
  register: result
  cisco.ios.ios_l2vpn_evpn:
    config:
      logging:
        peer_state: true
        vpws_vc_state: true
      replication_type: "ingress"
      flooding_suppression_address_resolution_disable: false
      router_id: "Loopback1"
      default_gateway_advertise: true
      multicast_advertise: true
    state: replaced

# Task Output:
# ------------
# "commands": [
#     "l2vpn evpn",
#     "replication-type ingress",
#     "no flooding-suppression address-resolution disable",
#     "no ip duplication limit 234 time 234",
#     "no mac duplication limit 213 time 123",
#     "router-id Loopback1",
#     "no multihoming aliasing disable",
#     "no ip local-learning disable",
#     "no ip local-learning limit per-mac ipv4 345",
#     "no ip local-learning limit per-mac ipv6 2345",
#     "no ip local-learning time down 234",
#     "no ip local-learning time poll 223",
#     "no ip local-learning time reachable 234",
#     "no ip local-learning time stale 23",
#     "no route-target auto vni",
#     "exit"
# ],
#
# After state:
# -------------
# l2vpn evpn
#  logging vpws vc-state
#  logging peer state
#  replication-type ingress
#  router-id Loopback1
#  default-gateway advertise
#  multicast advertise

# Using deleted

# Before state:
# -------------
# l2vpn evpn
#  logging vpws vc-state
#  logging peer state
#  replication-type static
#  flooding-suppression address-resolution disable
#  ip duplication limit 234 time 234
#  mac duplication limit 213 time 123
#  router-id Loopback0
#  multihoming aliasing disable
#  ip local-learning disable
#  ip local-learning limit per-mac ipv4 345
#  ip local-learning limit per-mac ipv6 2345
#  ip local-learning time down 234
#  ip local-learning time poll 223
#  ip local-learning time reachable 234
#  ip local-learning time stale 23
#  default-gateway advertise
#  route-target auto vni
#  multicast advertise

- name: Delete provided ios_l2vpn_evpn configuration
  register: result
  cisco.ios.ios_l2vpn_evpn:
    config:
      logging:
        peer_state: true
        vpws_vc_state: false
      replication_type: "static"
      flooding_suppression_address_resolution_disable: false
      ip_duplication:
        limit: 234
        time: 234
      mac_duplication:
        limit: 213
        time: 123
      router_id: "Loopback0"
      multihoming_aliasing_disable: true
    state: deleted

# Task Output:
# ------------
# "commands": [
#     "l2vpn evpn",
#     "no logging peer state",
#     "no replication-type static",
#     "no ip duplication limit 234 time 234",
#     "no mac duplication limit 213 time 123",
#     "no router-id Loopback0",
#     "no multihoming aliasing disable",
#     "exit"
# ],
#
# After state:
# -------------
# l2vpn evpn
#  logging vpws vc-state
#  flooding-suppression address-resolution disable
#  ip local-learning disable
#  ip local-learning limit per-mac ipv4 345
#  ip local-learning limit per-mac ipv6 2345
#  ip local-learning time down 234
#  ip local-learning time poll 223
#  ip local-learning time reachable 234
#  ip local-learning time stale 23
#  default-gateway advertise
#  route-target auto vni
#  multicast advertise
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
    - l2vpn evpn
    - no logging peer state
    - no replication-type static
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - l2vpn evpn
    - no logging peer state
    - no replication-type static
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.l2vpn_evpn.l2vpn_evpn import (
    L2vpn_evpnArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.l2vpn_evpn.l2vpn_evpn import (
    L2vpn_evpn,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=L2vpn_evpnArgs.argument_spec,
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

    result = L2vpn_evpn(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
