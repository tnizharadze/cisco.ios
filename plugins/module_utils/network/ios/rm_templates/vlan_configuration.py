# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Vlan_configuration parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from copy import deepcopy


class Vlan_configurationTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Vlan_configurationTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "vlan",
            "getval": re.compile(
                r"""
                vlan\sconfiguration\s(?P<vlan>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "vlan configuration {{ vlan }}",
            "result": {
                "{{ vlan }}": {
                    "vlan": "{{ vlan }}",
                },
            },
            "shared": True,
        },
        {
            "name": "member.vfi",
            "getval": re.compile(
                r"""
                \smember\svfi\s(?P<vfi>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "member vfi {{ member.vfi }}",
            "result": {
                "{{ vlan }}": {
                    "member": {
                        "vfi": "{{ vfi }}",
                    },
                },
            },
        },
        {
            "name": "member.access_vfi",
            "getval": re.compile(
                r"""
                \smember\saccess-vfi\s(?P<access_vfi>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "member access-vfi {{ member.access_vfi }}",
            "result": {
                "{{ vlan }}": {
                    "member": {
                        "access_vfi": "{{ access_vfi }}",
                    },
                },
            },
        },
        {
            "name": "member.vni",
            "getval": re.compile(
                r"""
                \smember\svni\s(?P<vni>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "member vni {{ member.vni }}",
            "result": {
                "{{ vlan }}": {
                    "member": {
                        "vni": "{{ vni }}",
                    },
                },
            },
        },
        {
            "name": "member.pseudowire",
            "getval": re.compile(
                r"""
                \smember\spseudowire(?P<pwnumber>\d+)
                (\s(?P<address>\S+)\s(?P<vc_id>\d+)\s
                ((template\s(?P<template>\S+))|
                (encapsulation\smpls)))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "member pseudowire{{ member.pseudowire.pwnumber }}"
                      "{% if member.pseudowire.address is defined and member.pseudowire.vc_id is defined %}"
                      " {{ member.pseudowire.address }} {{ member.pseudowire.vc_id }}"
                      "{% if member.pseudowire.template is defined %}"
                      " template {{ member.pseudowire.template }}"
                      "{% else %}"
                      " encapsulation mpls"
                      "{% endif %}"
                      "{% endif %}",
            "result": {
                "{{ vlan }}": {
                    "member": {
                        "pseudowire": {
                            "{{ pwnumber }}": {
                                "pwnumber": "{{ pwnumber }}",
                                "address": "{{ address }}",
                                "vc_id": "{{ vc_id }}",
                                "template": "{{ template }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "member.ip_peer",
            "getval": re.compile(
                r"""
                \smember\s
                (?P<address>(\s?((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})+)\s
                (?P<vc_id>\d+)\s
                ((template\s(?P<template>\S+))|
                (encapsulation\smpls))
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "member {{ member.ip_peer.address }} {{ member.ip_peer.vc_id }}"
                      "{% if member.ip_peer.template is defined %}"
                      " template {{ member.ip_peer.template }}"
                      "{% else %}"
                      " encapsulation mpls"
                      "{% endif %}",
            "result": {
                "{{ vlan }}": {
                    "member": {
                        "ip_peer": {
                            "{{ address ~ '_' ~ vc_id | replace('.','_') }}": {
                                "address": "{{ address }}",
                                "vc_id": "{{ vc_id }}",
                                "template": "{{ template }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "member.evpn",
            "getval": re.compile(
                r"""
                \smember\sevpn-instance\s(?P<instance>\S+)
                \svni\s(?P<vni>\S+)(?P<protected>\sprotected)?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "member evpn-instance {{ member.evpn.instance }} vni {{ member.evpn.vni }}"
                      "{% if member.evpn.protected is defined and member.evpn.protected %}"
                      " protected"
                      "{% endif %}",
            "result": {
                "{{ vlan }}": {
                    "member": {
                        "evpn": {
                            "instance": "{{ instance }}",
                            "vni": "{{ vni }}",
                            "protected": "{{ not not protected }}",
                        },
                    },
                },
            },
        },
        {
            "name": "device_tracking.enable",
            "getval": re.compile(
                r"""
                \s(?P<enable>device-tracking)
                (\sattach-policy\s(?P<attach_policy>\S+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "device-tracking"
                      "{% if device_tracking.attach_policy is defined %}"
                      " attach-policy {{ device_tracking.attach_policy }}"
                      "{% endif %}",
            "result": {
                "{{ vlan }}": {
                    "device_tracking": {
                        "enable": "{{ not not enable }}",
                        "attach_policy": "{{ attach_policy }}",
                    },
                },
            },
        },
        {
            "name": "mdns_sd_gateway.enable",
            "getval": re.compile(
                r"""
                \smdns-sd\s(?P<mdns_sd_gateway>gateway)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "mdns-sd gateway",
            "result": {
                "{{ vlan }}": {
                    "mdns_sd_gateway": {
                        "enable": "{{ not not mdns_sd_gateway }}"
                    },
                },
            },
        },
        {
            "name": "mdns_sd_gateway.active_query_timer",
            "getval": re.compile(
                r"""
                \s\sactive-query\stimer\s(?P<active_query_timer>\d+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "active-query timer {{ mdns_sd_gateway.active_query_timer }}",
            "result": {
                "{{ vlan }}": {
                    "mdns_sd_gateway": {
                        "active_query_timer": "{{ active_query_timer }}",
                    },
                },
            },
        },
        {
            "name": "mdns_sd_gateway.transport",
            "getval": re.compile(
                r"""
                \s\stransport\s(?P<transport>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "transport {{ mdns_sd_gateway.transport }}",
            "result": {
                "{{ vlan }}": {
                    "mdns_sd_gateway": {
                        "transport": "{{ transport }}",
                    },
                },
            },
        },
        {
            "name": "mdns_sd_gateway.service_inst_suffix",
            "getval": re.compile(
                r"""
                \s\sservice-inst-suffix\s(?P<service_inst_suffix>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "service-inst-suffix {{ mdns_sd_gateway.service_inst_suffix }}",
            "result": {
                "{{ vlan }}": {
                    "mdns_sd_gateway": {
                        "service_inst_suffix": "{{ service_inst_suffix }}",
                    },
                },
            },
        },
        {
            "name": "mdns_sd_gateway.service_mdns_query",
            "getval": re.compile(
                r"""
                \s\sservice-mdns-query\s(?P<service_mdns_query>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "service-mdns-query {{ mdns_sd_gateway.service_mdns_query }}",
            "result": {
                "{{ vlan }}": {
                    "mdns_sd_gateway": {
                        "service_mdns_query": "{{ service_mdns_query }}",
                    },
                },
            },
        },
        {
            "name": "mdns_sd_gateway.source_interface",
            "getval": re.compile(
                r"""
                \s\ssource-interface\s(?P<source_interface>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "source-interface {{ mdns_sd_gateway.source_interface }}",
            "result": {
                "{{ vlan }}": {
                    "mdns_sd_gateway": {
                        "source_interface": "{{ source_interface }}",
                    },
                },
            },
        },
        {
            "name": "mdns_sd_gateway.sdg_agent",
            "getval": re.compile(
                r"""
                \s\ssdg-agent\s(?P<sdg_agent>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "sdg-agent {{ mdns_sd_gateway.sdg_agent }}",
            "result": {
                "{{ vlan }}": {
                    "mdns_sd_gateway": {
                        "sdg_agent": "{{ sdg_agent }}",
                    },
                },
            },
        },
        {
            "name": "mdns_sd_gateway.service_policy",
            "getval": re.compile(
                r"""
                \s\sservice-policy\s(?P<service_policy>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "service-policy {{ mdns_sd_gateway.service_policy }}",
            "result": {
                "{{ vlan }}": {
                    "mdns_sd_gateway": {
                        "service_policy": "{{ service_policy }}",
                    },
                },
            },
        },
        {
            "name": "ipv6.destination_guard.enable",
            "getval": re.compile(
                r"""
                \sipv6\s(?P<enable>destination-guard)
                (\sattach-policy\s(?P<attach_policy>\S+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 destination-guard"
                      "{% if ipv6.destination_guard.attach_policy is defined %}"
                      " attach-policy {{ ipv6.destination_guard.attach_policy }}"
                      "{% endif %}",
            "result": {
                "{{ vlan }}": {
                    "ipv6": {
                        "destination_guard": {
                            "enable": "{{ not not enable }}",
                            "attach_policy": "{{ attach_policy }}",
                        },
                    },
                },
            },
        },
        {
            "name": "ipv6.dhcp.guard.enable",
            "getval": re.compile(
                r"""
                \sipv6\sdhcp\s(?P<enable>guard)
                (\sattach-policy\s(?P<attach_policy>\S+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 dhcp guard"
                      "{% if ipv6.dhcp.guard.attach_policy is defined %}"
                      " attach-policy {{ ipv6.dhcp.guard.attach_policy }}"
                      "{% endif %}",
            "result": {
                "{{ vlan }}": {
                    "ipv6": {
                        "dhcp": {
                            "guard": {
                                "enable": "{{ not not enable }}",
                                "attach_policy": "{{ attach_policy }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ipv6.dhcp.ldra_attach_policy",
            "getval": re.compile(
                r"""
                \sipv6\sdhcp\sldra\sattach-policy\s(?P<attach_policy>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 dhcp ldra attach-policy {{ ipv6.dhcp.ldra_attach_policy }}",
            "result": {
                "{{ vlan }}": {
                    "ipv6": {
                        "dhcp": {
                            "ldra_attach_policy": "{{ attach_policy }}",
                        },
                    },
                },
            },
        },
        {
            "name": "ipv6.nd.ra_throttler.enable",
            "getval": re.compile(
                r"""
                \sipv6\snd\s(?P<enable>ra-throttler)
                (\sattach-policy\s(?P<attach_policy>\S+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 nd ra-throttler"
                      "{% if ipv6.nd.ra_throttler.attach_policy is defined %}"
                      " attach-policy {{ ipv6.nd.ra_throttler.attach_policy }}"
                      "{% endif %}",
            "result": {
                "{{ vlan }}": {
                    "ipv6": {
                        "nd": {
                            "ra_throttler": {
                                "enable": "{{ not not enable }}",
                                "attach_policy": "{{ attach_policy }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ipv6.nd.raguard.enable",
            "getval": re.compile(
                r"""
                \sipv6\snd\s(?P<enable>raguard)
                (\sattach-policy\s(?P<attach_policy>\S+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 nd raguard"
                      "{% if ipv6.nd.raguard.attach_policy is defined %}"
                      " attach-policy {{ ipv6.nd.raguard.attach_policy }}"
                      "{% endif %}",
            "result": {
                "{{ vlan }}": {
                    "ipv6": {
                        "nd": {
                            "raguard": {
                                "enable": "{{ not not enable }}",
                                "attach_policy": "{{ attach_policy }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ipv6.nd.suppress.enable",
            "getval": re.compile(
                r"""
                \sipv6\snd\s(?P<enable>suppress)
                (\sattach-policy\s(?P<attach_policy>\S+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 nd suppress"
                      "{% if ipv6.nd.suppress.attach_policy is defined %}"
                      " attach-policy {{ ipv6.nd.suppress.attach_policy }}"
                      "{% endif %}",
            "result": {
                "{{ vlan }}": {
                    "ipv6": {
                        "nd": {
                            "suppress": {
                                "enable": "{{ not not enable }}",
                                "attach_policy": "{{ attach_policy }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "et_analytics_enable",
            "getval": re.compile(
                r"""
                \set-analytics\s(?P<et_analytics_enable>enable)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "et-analytics enable",
            "result": {
                "{{ vlan }}": {
                    "et_analytics_enable": "{{ not not et_analytics_enable }}"
                },
            },
        },
    ]
    # fmt: on
