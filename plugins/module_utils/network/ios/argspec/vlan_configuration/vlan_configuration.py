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
The arg spec for the ios_vlan_configuration module
"""


class Vlan_configurationArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_vlan_configuration module
    """

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "vlan": {"type": "str", "required": True},
                "member": {
                    "type": "dict",
                    "mutually_exclusive": [
                        ["vfi", "access_vfi"],
                        ["vni","vfi","evpn"],
                    ],
                    "options": {
                        "vfi": {"type": "str"},
                        "access_vfi": {"type": "str"},
                        "vni": {"type": "str"},
                        "ip_peer": {
                            "type": "list",
                            "elements": "dict",
                            "required_together": [["address", "vc_id"]],
                            "options": {
                                "address": {"type": "str"},
                                "vc_id": {"type": "str"},
                                "template": {"type": "str"},
                            },
                        },
                        "pseudowire": {
                            "type": "list",
                            "elements": "dict",
                            "required_together": [["address", "vc_id"]],
                            "options": {
                                "pwnumber": {"type": "str"},
                                "address": {"type": "str"},
                                "vc_id": {"type": "str"},
                                "template": {"type": "str"},
                            },
                        },
                        "evpn": {
                            "type": "dict",
                            "required_together": [["instance", "vni"]],
                            "options": {
                                "instance": {"type": "str", "required": True},
                                "vni": {"type": "str"},
                                "protected": {"type": "bool"},
                            },
                        },
                    },
                },
                "mdns_sd_gateway": {
                    "type": "dict",
                    "options": {
                        "enable": {"type": "bool", "required": True},
                        "active_query_timer": {"type": "str"},
                        "transport": {
                            "type": "str",
                            "choices": ["ipv4", "ipv6", "both"],
                        },
                        "service_inst_suffix": {"type": "str"},
                        "service_mdns_query": {
                            "type": "str",
                            "choices": ["ptr", "all"],
                        },
                        "source_interface": {"type": "str"},
                        "sdg_agent": {"type": "str"},
                        "service_policy": {"type": "str"},
                    },
                },
                "et_analytics_enable": {"type": "bool"},
                "device_tracking": {
                    "type": "dict",
                    "required_by": {"attach_policy": "enable"},
                    "options": {
                        "enable": {"type": "bool"},
                        "attach_policy": {"type": "str"},
                    },
                },
                "ipv6": {
                    "type": "dict",
                    "options": {
                        "destination_guard": {
                            "type": "dict",
                            "required_by": {"attach_policy": "enable"},
                            "options": {
                                "enable": {"type": "bool"},
                                "attach_policy": {"type": "str"},
                            },
                        },
                        "dhcp": {
                            "type": "dict",
                            "options": {
                                "guard": {
                                    "type": "dict",
                                    "required_by": {"attach_policy": "enable"},
                                    "options": {
                                        "enable": {"type": "bool"},
                                        "attach_policy": {"type": "str"},
                                    },
                                },
                                "ldra_attach_policy": {
                                    "type": "str",
                                    "choices": [
                                        "client-facing-trusted",
                                        "client-facing-untrusted",
                                    ],
                                },
                            },
                        },
                        "nd": {
                            "type": "dict",
                            "options": {
                                "ra_throttler": {
                                    "type": "dict",
                                    "required_by": {"attach_policy": "enable"},
                                    "options": {
                                        "enable": {"type": "bool"},
                                        "attach_policy": {"type": "str"},
                                    },
                                },
                                "raguard": {
                                    "type": "dict",
                                    "required_by": {"attach_policy": "enable"},
                                    "options": {
                                        "enable": {"type": "bool"},
                                        "attach_policy": {"type": "str"},
                                    },
                                },
                                "suppress": {
                                    "type": "dict",
                                    "required_by": {"attach_policy": "enable"},
                                    "options": {
                                        "enable": {"type": "bool"},
                                        "attach_policy": {"type": "str"},
                                    },
                                },
                            },
                        },
                    },
                },
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
