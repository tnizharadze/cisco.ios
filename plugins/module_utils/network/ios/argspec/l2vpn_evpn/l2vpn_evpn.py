# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the
# cli_rm_builder.
#
# Manually editing this file is not advised.
#
# To update the argspec make the desired changes
# in the module docstring and re-run
# cli_rm_builder.
#
#############################################

"""
The arg spec for the ios_l2vpn_evpn module
"""


class L2vpn_evpnArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_l2vpn_evpn module
    """

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "logging": {
                    "type": "dict",
                    "options": {
                        "peer_state": {"type": "bool"},
                        "vpws_vc_state": {"type": "bool"},
                    },
                },
                "replication_type": {
                    "type": "str",
                    "choices": ["static", "ingress"],
                },
                "flooding_suppression_address_resolution_disable": {
                    "type": "bool"
                },
                "ip_duplication": {
                    "type": "dict",
                    "required_together": [["limit", "time"]],
                    "options": {"limit": {"type": "int"}, "time": {"type": "int"}},
                },
                "mac_duplication": {
                    "type": "dict",
                    "required_together": [["limit", "time"]],
                    "options": {"limit": {"type": "int"}, "time": {"type": "int"}},
                },
                "router_id": {"type": "str"},
                "multihoming_aliasing_disable": {"type": "bool"},
                "ip_local_learning": {
                    "type": "dict",
                    "options": {
                        "disable": {"type": "bool"},
                        "limit_per_mac_ipv4": {"type": "int"},
                        "limit_per_mac_ipv6": {"type": "int"},
                        "time": {
                            "type": "dict",
                            "options": {
                                "down": {"type": "int"},
                                "poll": {"type": "int"},
                                "reachable": {"type": "int"},
                                "stale": {"type": "int"},
                            },
                        },
                    },
                },
                "default_gateway_advertise": {"type": "bool"},
                "route_target_auto_vni": {"type": "bool"},
                "multicast_advertise": {"type": "bool"},
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
            "choices": [
                "merged",
                "replaced",
                "deleted",
                "rendered",
                "parsed",
                "gathered",
            ],
            "default": "merged",
        },
    }  # pylint: disable=C0301
