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

    def parse(self):
        """parse"""
        result = {}
        shared = {}
        for line in self._lines:
            for parser in self._tmplt.PARSERS:
                cap = re.match(parser["getval"], line)
                if cap:
                    capdict = cap.groupdict()
                    capdict = dict(
                        (k, v) for k, v in capdict.items() if v is not None
                    )
                    if parser.get("shared"):
                        shared = dict_merge(shared, capdict)
                    vals = dict_merge(capdict, shared)
                    res = self._deepformat(deepcopy(parser["result"]), vals)
                    result = dict_merge(result, res)
                    break
        return result

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
            "name": "vfi",
            "getval": re.compile(
                r"""
                \smember\svfi\s(?P<vfi>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "member vfi {{ vfi }}",
            "result": {
                "{{ vlan }}": {
                    "member": {
                        "vfi": "{{ vfi }}",
                    },
                },
            },
        },
        {
            "name": "access_vfi",
            "getval": re.compile(
                r"""
                \smember\saccess-vfi\s(?P<access_vfi>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "member access-vfi {{ access_vfi }}",
            "result": {
                "{{ vlan }}": {
                    "member": {
                        "access_vfi": "{{ access_vfi }}",
                    },
                },
            },
        },
        {
            "name": "pwnumber",
            "getval": re.compile(
                r"""
                \smember\spseudowire(?P<pwnumber>\d+)
                (\s(?P<address>\S+)\s(?P<vc_id>\d+)\s
                (template\s(?P<template>\S+))?
                (encapsulation\s(?P<encapsulation_mpls>mpls))?)?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "member pseudowire{{ pwnumber }}"
                      "{% if address is defined and vc_id is defined %}"
                      " {{ address }} {{ vc_id }}"
                      "{% if template is defined %}"
                      " template {{ template }}"
                      "{% elif encapsulation_mpls is defined and encapsulation_mpls %}"
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
                                "encapsulation_mpls": "{{ not not encapsulation_mpls }}",
                            },
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
