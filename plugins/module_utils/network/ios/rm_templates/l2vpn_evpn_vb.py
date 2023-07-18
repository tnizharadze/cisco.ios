# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The L2vpn_evpn_vb parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class L2vpn_evpn_vbTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(L2vpn_evpn_vbTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "instance",
            "getval": re.compile(
                r"""
                l2vpn\sevpn\sinstance\s(?P<instance>\S+)\svlan-based
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "l2vpn evpn instance {{ instance }} vlan-based",
            "result": {
                "{{ instance }}": {
                    "instance": "{{ instance }}",
                },
            },
            "shared": True,
        },
        {
            "name": "encapsulation",
            "getval": re.compile(
                r"""
                \sencapsulation\s(?P<encapsulation>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "encapsulation {{ encapsulation }}",
            "result": {
                "{{ instance }}": {
                    "encapsulation": "{{ encapsulation }}",
                },
            },
        },
        {
            "name": "rd",
            "getval": re.compile(
                r"""
                \srd\s(?P<rd>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "rd {{ rd }}",
            "result": {
                "{{ instance }}": {
                    "rd": "{{ rd }}",
                },
            },
        },
        {
            "name": "route_target_import",
            "getval": re.compile(
                r"""
                \sroute-target\simport\s(?P<route_target_import>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "route-target import {{ route_target_import }}",
            "result": {
                "{{ instance }}": {
                    "route_target_import": ["{{ route_target_import }}"],
                },
            },
        },
        {
            "name": "route_target_export",
            "getval": re.compile(
                r"""
                \sroute-target\sexport\s(?P<route_target_export>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "route-target export {{ route_target_export }}",
            "result": {
                "{{ instance }}": {
                    "route_target_export": ["{{ route_target_export }}"],
                },
            },
        },
        {
            "name": "auto_route_target",
            "getval": re.compile(
                r"""
                \s(?P<negated>no\s)?(?P<auto_route_target>auto-route-target)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "auto-route-target",
            "result": {
                "{{ instance }}": {
                    "auto_route_target": "{{ False if negated is defined else not not auto_route_target|d(True) }}",
                },
            },
        },
        {
            "name": "replication_type",
            "getval": re.compile(
                r"""
                \sreplication-type\s(?P<replication_type>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "replication-type {{ replication_type }}",
            "result": {
                "{{ instance }}": {
                    "replication_type": "{{ replication_type }}",
                },
            },
        },
        {
            "name": "ip_local_learning",
            "getval": re.compile(
                r"""
                \sip\slocal-learning\s(?P<ip_local_learning>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ip local-learning {{ ip_local_learning }}",
            "result": {
                "{{ instance }}": {
                    "ip_local_learning": "{{ ip_local_learning }}",
                },
            },
        },
        {
            "name": "default_gateway_advertise",
            "getval": re.compile(
                r"""
                \sdefault-gateway\sadvertise\s(?P<default_gateway_advertise>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "default-gateway advertise {{ default_gateway_advertise }}",
            "result": {
                "{{ instance }}": {
                    "default_gateway_advertise": "{{ default_gateway_advertise }}",
                },
            },
        },
        {
            "name": "multicast_advertise",
            "getval": re.compile(
                r"""
                \smulticast\sadvertise\s(?P<multicast_advertise>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "multicast advertise {{ multicast_advertise }}",
            "result": {
                "{{ instance }}": {
                    "multicast_advertise": "{{ multicast_advertise }}",
                },
            },
        },
        {
            "name": "re_originate_route_type5",
            "getval": re.compile(
                r"""
                \sre-originate\s(?P<re_originate_route_type5>route-type5)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "re-originate route-type5",
            "result": {
                "{{ instance }}": {
                    "re_originate_route_type5": "{{ not not re_originate_route_type5 }}",
                },
            },
        },
    ]
    # fmt: on
