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
The arg spec for the ios_spanning_tree module
"""


class Spanning_treeArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_spanning_tree module
    """

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "spanning_tree": {
                    "type": "dict",
                    "options": {
                        "backbonefast": {"type": "bool"},
                        "bridge_assurance": {"type": "bool"},
                        "etherchannel_guard_misconfig": {"type": "bool"},
                        "extend_system_id": {"type": "bool"},
                        "logging": {"type": "bool"},
                        "loopguard_default": {"type": "bool"},
                        "mode": {
                            "type": "str",
                            "choices": ["mst", "pvst", "rapid-pvst"],
                        },
                        "pathcost_method": {
                            "type": "str",
                            "choices": ["long", "short"],
                        },
                        "transmit_hold_count": {"type": "int"},
                        "portfast": {
                            "type": "dict",
                            "mutually_exclusive": [
                                ["network_default", "edge_default"]
                            ],
                            "options": {
                                "network_default": {"type": "bool"},
                                "edge_default": {"type": "bool"},
                                "bpdufilter_default": {"type": "bool"},
                                "bpduguard_default": {"type": "bool"},
                            },
                        },
                        "uplinkfast": {
                            "type": "dict",
                            "options": {
                                "enabled": {"type": "bool"},
                                "max_update_rate": {"type": "int"},
                            },
                        },
                        "forward_time": {
                            "type": "dict",
                            "required_together": ["vlan_list", "value"],
                            "options": {
                                "vlan_list": {"type": "list", "elements": "int"},
                                "value": {"type": "int"},
                            },
                        },
                        "hello_time": {
                            "type": "dict",
                            "required_together": ["vlan_list", "value"],
                            "options": {
                                "vlan_list": {"type": "list", "elements": "int"},
                                "value": {"type": "int"},
                            },
                        },
                        "max_age": {
                            "type": "dict",
                            "required_together": ["vlan_list", "value"],
                            "options": {
                                "vlan_list": {"type": "list", "elements": "int"},
                                "value": {"type": "int"},
                            },
                        },
                        "priority": {
                            "type": "dict",
                            "required_together": ["vlan_list", "value"],
                            "options": {
                                "vlan_list": {"type": "list", "elements": "int"},
                                "value": {
                                    "type": "int",
                                    "choices": [
                                        0,
                                        4096,
                                        8192,
                                        12288,
                                        16384,
                                        20480,
                                        24576,
                                        28672,
                                        32768,
                                        36864,
                                        40960,
                                        45056,
                                        49152,
                                        53248,
                                        57344,
                                        61440,
                                    ],
                                },
                            },
                        },
                    },
                }
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
