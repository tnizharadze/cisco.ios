# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The L2vpn_evpn_ptp parser templates file. This contains
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


class L2vpn_evpn_ptpTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(L2vpn_evpn_ptpTemplate, self).__init__(lines=lines, tmplt=self, module=module)

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
            "name": "instance",
            "getval": re.compile(
                r"""
                l2vpn\sevpn\sinstance\s(?P<instance>\S+)\spoint-to-point
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "l2vpn evpn instance {{ instance }} point-to-point",
            "result": {
                "{{ instance }}": {
                    "instance": "{{ instance }}",
                },
            },
            "shared": True,
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
            "name": "context",
            "getval": re.compile(
                r"""
                \svpws\scontext\s(?P<context>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "vpws context {{ context }}",
            "result": {
                "{{ instance }}": {
                    "vpws_context": {
                        "{{ context }}": {
                            "context": "{{ context }}",
                        },
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "service",
            "getval": re.compile(
                r"""
                \s\sservice\starget\s(?P<target>\S+)\ssource\s(?P<source>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "service target {{ service.target }} source {{ service.source }}",
            "result": {
                "{{ instance }}": {
                    "vpws_context": {
                        "{{ context }}": {
                            "service": {
                                "target": "{{ target }}",
                                "source": "{{ source }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "member",
            "getval": re.compile(
                r"""
                \s\smember\s(?P<member>\S+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "member {{ member }}",
            "result": {
                "{{ instance }}": {
                    "vpws_context": {
                        "{{ context }}": {
                            "member": "{{ member }}",
                        },
                    },
                },
            },
        },
        {
            "name": "remote_link_failure_notification",
            "getval": re.compile(
                r"""
                \s\sremote\slink\sfailure\s(?P<remote_link_failure_notification>notification)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "remote link failure notification",
            "result": {
                "{{ instance }}": {
                    "vpws_context": {
                        "{{ context }}": {
                            "remote_link_failure_notification": "{{ not not remote_link_failure_notification }}",
                        },
                    },
                },
            },
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""
                \s\s(?P<shutdown>shutdown)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "shutdown",
            "result": {
                "{{ instance }}": {
                    "vpws_context": {
                        "{{ context }}": {
                            "shutdown": "{{ not not shutdown }}",
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
