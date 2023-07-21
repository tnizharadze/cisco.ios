#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function
from telnetlib import NOP

__metaclass__ = type

"""
The ios_l2vpn_evpn_ptp config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
    get_from_dict,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.l2vpn_evpn_ptp import (
    L2vpn_evpn_ptpTemplate,
)


class L2vpn_evpn_ptp(ResourceModule):
    """
    The ios_l2vpn_evpn_ptp config class
    """

    def __init__(self, module):
        super(L2vpn_evpn_ptp, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="l2vpn_evpn_ptp",
            tmplt=L2vpn_evpn_ptpTemplate(),
        )
        self.sequence_parsers = [
            "instance",
            "context",
        ]
        self.linear_parsers = [
            "rd",
            "service",
            "member",
            "remote_link_failure_notification",
            "shutdown",
        ]
        self.negated_parsers = [
            "auto_route_target",
        ]
        self.list_parsers = [
            "route_target_import",
            "route_target_export",
        ]

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """ Generate configuration commands to send based on
            want, have and desired state.
        """
        wantd = self._l2vpn_list_to_dict(self.want)
        haved = self._l2vpn_list_to_dict(self.have)
#        raise Exception([wantd, haved])
        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        if self.state == "deleted":
            haved = self._dict_copy_deleted(wantd, haved)
            self._delete_entries(haved)
            wantd = {}

        if wantd:
            self._compare_config(wantd, haved)

    def _delete_entries(self, haved):
        for hk, have in iteritems(haved):
            current = ""
            for x in self.sequence_parsers:
                if x in have:
                    current = x
            if "_remove" in have:
                self.commands.append(self._tmplt.render(have, current, True))
                if current == "instance":
                    cmd = self.commands.pop()
                    self.commands.append({"command": cmd, "prompt": "yes/no", "answer": "yes"})
                continue
            begin = len(self.commands)
            self._compare_lists({}, have)
            self._compare_negated({}, have)
            self.compare(parsers=self.linear_parsers, want={}, have=have)
            if "vpws_context" in have:
                self._delete_entries(have["vpws_context"])
            if len(self.commands) != begin:
                self.commands.insert(begin, self._tmplt.render(have, current, False))
                self.commands.append("exit")

    def _compare_config(self, wantd, haved):
        for hk, have in iteritems(haved):
            current = ""
            for x in self.sequence_parsers:
                if x in have:
                    current = x
            if hk not in wantd:
                self.commands.append(self._tmplt.render(have, current, True))
                if current == "instance":
                    cmd = self.commands.pop()
                    self.commands.append({"command": cmd, "prompt": "yes/no", "answer": "yes"})
        for wk, want in iteritems(wantd):
            current = ""
            for x in self.sequence_parsers:
                if x in want:
                    current = x
            have = haved.get(wk) or {}
            begin = len(self.commands)
            self._compare_lists(want, have)
            self._compare_negated(want, have)
            self._compare_member(want, have)
            self.compare(parsers=self.linear_parsers, want=want, have=have)
            if "vpws_context" in want:
                self._compare_config(want["vpws_context"], have.get("vpws_context") or {})
            if len(self.commands) != begin:
                self.commands.insert(begin, self._tmplt.render(want, current, False))
                self.commands.append("exit")

    def _compare_lists(self, want, have):
        for x in self.list_parsers:
            wx = set(get_from_dict(want, x) or [])
            hx = set(get_from_dict(have, x) or [])
            wdiff = sorted(list(wx - hx))
            hdiff = sorted(list(hx - wx))
            for each in hdiff:
                self.commands.append(self._tmplt.render({x: each}, x, True))
            for each in wdiff:
                self.commands.append(self._tmplt.render({x: each}, x, False))

    def _compare_negated(self, want, have):
        for x in self.negated_parsers:
            if x in want and x not in have:
                self.compare(parsers=[x], want=want, have={x: True})
            else:
                self.compare(parsers=[x], want=want, have=have)

    def _compare_member(self, want, have):
        # avoid IOS error "Only one member allowed in a EVPN VPWS context"
        # by deleting have["member"]
        if "member" in want and "member" in have \
                and want["member"] != have["member"]:
            self.compare(parsers=["member"], want={}, have=have)

    def _dict_copy_deleted(self, want, have, x=""):
        hrec = {}
        have_dict = have if x == "" else get_from_dict(have, x)
        want_dict = want if x == "" else get_from_dict(want, x)
        for k, hx in iteritems(have_dict):
            if not want:
                hrec.update({k: hx})
                hrec[k].update({"_remove": True})
                continue
            dstr = k if x == "" else x + "." + k
            wx = get_from_dict(want, dstr)
            if wx is None:
                continue
            if isinstance(wx, dict):
                hrec.update({k: self._dict_copy_deleted(want, have, dstr)})
            elif isinstance(wx, list):
                wsect = set(wx).intersection(set(hx))
                if wsect:
                    hrec.update({k: sorted(list(wsect))})
            elif k in self.sequence_parsers and (have_dict == want_dict):
                return {k: hx, "_remove": True}
            elif k in self.negated_parsers and hx and wx:
                continue
            elif wx == hx:
                hrec.update({k: hx})
        return hrec

    def _l2vpn_list_to_dict(self, entry):
        for x in entry:
            for k, val in iteritems(x):
                if isinstance(val, list):
                    if k == "vpws_context":
                        x["vpws_context"] = {i["context"]: i for i in val}
                    else:
                        x[k] = sorted(val)
        entry = {x["instance"]: x for x in entry}
        return entry
