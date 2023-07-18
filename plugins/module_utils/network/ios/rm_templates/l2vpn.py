# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The L2vpn parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class L2vpnTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(L2vpnTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "logging.pseudowire_status",
            "getval": re.compile(
                r"""
                \slogging\spseudowire\s(?P<pseudowire_status>status)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "logging pseudowire status",
            "result": {
                "logging": {
                    "pseudowire_status": "{{ not not pseudowire_status }}",
                },
            },
        },
        {
            "name": "logging.redundancy",
            "getval": re.compile(
                r"""
                \slogging\s(?P<redundancy>redundancy)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "logging redundancy",
            "result": {
                "logging": {
                    "redundancy": "{{ not not redundancy }}",
                },
            },
        },
        {
            "name": "logging.vc_state",
            "getval": re.compile(
                r"""
                \slogging\s(?P<vc_state>vc-state)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "logging vc-state",
            "result": {
                "logging": {
                    "vc_state": "{{ not not vc_state }}",
                },
            },
        },
        {
            "name": "redundancy_predictive_enabled",
            "getval": re.compile(
                r"""
                \sredundancy\spredictive\s(?P<redundancy_predictive_enabled>enabled)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "redundancy predictive enabled",
            "result": {
                "redundancy_predictive_enabled": "{{ not not redundancy_predictive_enabled }}",
            },
        },
        {
            "name": "pseudowire_group_status",
            "getval": re.compile(
                r"""
                \spseudowire\sgroup\s(?P<pseudowire_group_status>status)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "pseudowire group status",
            "result": {
                "pseudowire_group_status": "{{ not not pseudowire_group_status }}",
            },
        },
        {
            "name": "router_id",
            "getval": re.compile(
                r"""
                \srouter-id\s(?P<router_id>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "router-id {{ router_id }}",
            "result": {
                "router_id": "{{ router_id }}",
            },
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""
                \s(?P<shutdown>shutdown)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "shutdown",
            "result": {
                "shutdown": "{{ not not shutdown }}",
            },
        },
    ]
    # fmt: on
