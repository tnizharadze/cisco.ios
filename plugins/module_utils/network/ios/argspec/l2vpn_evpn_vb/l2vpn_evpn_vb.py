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
The arg spec for the ios_l2vpn_evpn_vb module
"""


class L2vpn_evpn_vbArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_l2vpn_evpn_vb module
    """

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "instance": {"type": "int"},
                "auto_route_target": {"type": "bool", "default": True},
                "default_gateway_advertise": {
                    "type": "str",
                    "choices": ["enable", "disable"],
                },
                "encapsulation": {"type": "str", "choices": ["vxlan"]},
                "ip_local_learning": {
                    "type": "str",
                    "choices": ["enable", "disable"],
                },
                "multicast_advertise": {
                    "type": "str",
                    "choices": ["enable", "disable"],
                },
                "rd": {"type": "str"},
                "re_originate_route_type5": {"type": "bool"},
                "replication_type": {
                    "type": "str",
                    "choices": ["static", "ingress"],
                },
                "route_target_import": {"type": "list", "elements": "str"},
                "route_target_export": {"type": "list", "elements": "str"},
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
