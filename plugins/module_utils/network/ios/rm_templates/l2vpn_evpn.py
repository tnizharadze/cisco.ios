# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The L2vpn_evpn parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)

class L2vpn_evpnTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(L2vpn_evpnTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "logging.vpws_vc_state",
            "getval": re.compile(
                r"""
                \slogging\svpws\s(?P<vpws_vc_state>vc-state)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "logging vpws vc-state",
            "result": {
                "logging": {
                    "vpws_vc_state": "{{ not not vpws_vc_state }}", 
                },
            },
        },
        {
            "name": "logging.peer_state",
            "getval": re.compile(
                r"""
                \slogging\speer\s(?P<peer_state>state)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "logging peer state",
            "result": {
                "logging": {
                    "peer_state": "{{ not not peer_state }}", 
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
                "replication_type": "{{ replication_type }}", 
            },
        },
        {
            "name": "flooding_suppression_address_resolution_disable",
            "getval": re.compile(
                r"""
                \sflooding-suppression\saddress-resolution\s(?P<flooding_suppression_address_resolution_disable>disable)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "flooding-suppression address-resolution disable",
            "result": {
                "flooding_suppression_address_resolution_disable": "{{ not not flooding_suppression_address_resolution_disable }}", 
            },
        },
        {
            "name": "ip_duplication",
            "getval": re.compile(
                r"""
                \sip\sduplication\slimit\s(?P<limit>\S+)\stime\s(?P<time>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ip duplication limit {{ ip_duplication.limit }} time {{ ip_duplication.time }}",
            "result": {
                "ip_duplication": {
                    "limit": "{{ limit | int }}",
                    "time": "{{ time | int }}",
                }, 
            },
        },
        {
            "name": "mac_duplication",
            "getval": re.compile(
                r"""
                \smac\sduplication\slimit\s(?P<limit>\S+)\stime\s(?P<time>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "mac duplication limit {{ mac_duplication.limit }} time {{ mac_duplication.time }}",
            "result": {
                "mac_duplication": {
                    "limit": "{{ limit | int }}",
                    "time": "{{ time | int }}",
                }, 
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
            "name": "multihoming_aliasing_disable",
            "getval": re.compile(
                r"""
                \smultihoming\saliasing\s(?P<multihoming_aliasing_disable>disable)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "multihoming aliasing disable",
            "result": {
                "multihoming_aliasing_disable": "{{ not not multihoming_aliasing_disable }}", 
            },
        },
        {
            "name": "ip_local_learning.disable",
            "getval": re.compile(
                r"""
                \sip\slocal-learning\s(?P<disable>disable)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ip local-learning disable",
            "result": {
                "ip_local_learning": {
                    "disable": "{{ not not disable }}",
                },
            },
        },
        {
            "name": "ip_local_learning.limit_per_mac_ipv4",
            "getval": re.compile(
                r"""
                \sip\slocal-learning\slimit\sper-mac\sipv4\s(?P<limit_per_mac_ipv4>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ip local-learning limit per-mac ipv4 {{ ip_local_learning.limit_per_mac_ipv4 }}",
            "result": {
                "ip_local_learning": {
                    "limit_per_mac_ipv4": "{{ limit_per_mac_ipv4 | int }}",
                },
            },
        },
        {
            "name": "ip_local_learning.limit_per_mac_ipv6",
            "getval": re.compile(
                r"""
                \sip\slocal-learning\slimit\sper-mac\sipv6\s(?P<limit_per_mac_ipv6>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ip local-learning limit per-mac ipv6 {{ ip_local_learning.limit_per_mac_ipv6 }}",
            "result": {
                "ip_local_learning": {
                    "limit_per_mac_ipv6": "{{ limit_per_mac_ipv6 | int }}",
                }, 
            },
        },
        {
            "name": "ip_local_learning.time.down",
            "getval": re.compile(
                r"""
                \sip\slocal-learning\stime\sdown\s(?P<down>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ip local-learning time down {{ ip_local_learning.time.down }}",
            "result": {
                "ip_local_learning": {
                    "time": {
                        "down": "{{ down | int }}",
                    },
                }, 
            },
        },
        {
            "name": "ip_local_learning.time.poll",
            "getval": re.compile(
                r"""
                \sip\slocal-learning\stime\spoll\s(?P<poll>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ip local-learning time poll {{ ip_local_learning.time.poll }}",
            "result": {
                "ip_local_learning": {
                    "time": {
                        "poll": "{{ poll | int }}",
                    },
                }, 
            },
        },
        {
            "name": "ip_local_learning.time.reachable",
            "getval": re.compile(
                r"""
                \sip\slocal-learning\stime\sreachable\s(?P<reachable>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ip local-learning time reachable {{ ip_local_learning.time.reachable }}",
            "result": {
                "ip_local_learning": {
                    "time": {
                        "reachable": "{{ reachable | int }}",
                    },
                }, 
            },
        },
        {
            "name": "ip_local_learning.time.stale",
            "getval": re.compile(
                r"""
                \sip\slocal-learning\stime\sstale\s(?P<stale>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ip local-learning time stale {{ ip_local_learning.time.stale }}",
            "result": {
                "ip_local_learning": {
                    "time": {
                        "stale": "{{ stale | int }}",
                    },
                }, 
            },
        },
        {
            "name": "default_gateway_advertise",
            "getval": re.compile(
                r"""
                \sdefault-gateway\s(?P<default_gateway_advertise>advertise)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "default-gateway advertise",
            "result": {
                "default_gateway_advertise": "{{ not not default_gateway_advertise }}", 
            },
        },
        {
            "name": "route_target_auto_vni",
            "getval": re.compile(
                r"""
                \sroute-target\sauto\s(?P<route_target_auto_vni>vni)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "route-target auto vni",
            "result": {
                "route_target_auto_vni": "{{ not not route_target_auto_vni }}", 
            },
        },
        {
            "name": "multicast_advertise",
            "getval": re.compile(
                r"""
                \smulticast\s(?P<multicast_advertise>advertise)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "multicast advertise",
            "result": {
                "multicast_advertise": "{{ not not multicast_advertise }}", 
            },
        },
    ]
    # fmt: on
