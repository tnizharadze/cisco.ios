#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function
from telnetlib import NOP
from pickle import TRUE

__metaclass__ = type

"""
The ios_vlan_configuration config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.vlan_configuration import (
    Vlan_configurationTemplate,
)


class Vlan_configuration(ResourceModule):
    """
    The ios_vlan_configuration config class
    """

    def __init__(self, module):
        super(Vlan_configuration, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="vlan_configuration",
            tmplt=Vlan_configurationTemplate(),
        )
        self.sequence_parsers = [
            "vlan",
        ]
        self.dict_parsers = [
            "member.pseudowire",
            "member.ip_peer",
        ]
        self.linear_parsers = [
            "member.vfi",
            "member.access_vfi",
            "member.vni",
            "member.evpn",
            "ipv6.dhcp.ldra_attach_policy",
            "et_analytics_enable",
        ]
        self.dual_parsers = [
            "device_tracking",
            "ipv6.destination_guard",
            "ipv6.dhcp.guard",
            "ipv6.nd.ra_throttler",
            "ipv6.nd.raguard",
            "ipv6.nd.suppress",
        ]
        self.mdns_parsers = [
            "mdns_sd_gateway.active_query_timer",
            "mdns_sd_gateway.transport",
            "mdns_sd_gateway.service_inst_suffix",
            "mdns_sd_gateway.service_mdns_query",
            "mdns_sd_gateway.source_interface",
            "mdns_sd_gateway.sdg_agent",
            "mdns_sd_gateway.service_policy",
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
        wantd = self._list_to_dict(self.want)
        haved = self._list_to_dict(self.have)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        if self.state == "deleted":
            haved = self._dict_copy_deleted(wantd, haved)
            self._delete_entries(haved)
            wantd = {}

        if wantd:
            self._compare_config(wantd, haved)

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
            #if k == "ip_peer":
            #    import pydevd; pydevd.settrace()
            wx = get_from_dict(want, dstr)
            if wx is None:
                continue
            dp = False
            for i in self.dual_parsers:
                if i in dstr: dp = True
            if dp and wx == hx:
                hrec.update({k: hx})
            elif dp:
                continue
            elif k == "mdns_sd_gateway" and wx == hx:
                hrec.update({k: {"enable": True}})
            elif isinstance(wx, dict):
                hrec.update({k: self._dict_copy_deleted(want, have, dstr)})
            elif k == "vlan" and (have_dict == want_dict):
                return {k: hx, "_remove": True}
            elif wx == hx:
                hrec.update({k: hx})
        return hrec

    def _delete_entries(self, haved):
        for hk, have in iteritems(haved):
            if "_remove" in have:
                self.commands.append(self._tmplt.render(have, "vlan", True))
                continue
            begin = len(self.commands)
            for x in self.dict_parsers:
                hx = get_from_dict(have, x) or {}
                self._compare_dict({}, hx, x)
            self.compare(parsers=self.linear_parsers, want={}, have=have)
            self._compare_dual({}, have)
            want = {}
            if "mdns_sd_gateway" in have and len(have["mdns_sd_gateway"]) > 1:
                have["mdns_sd_gateway"].pop("enable")
                want = self._construct_dict("mdns_sd_gateway", {"enable": True})
            self._compare_mdns(want, have)
            if len(self.commands) != begin:
                self.commands.insert(begin, self._tmplt.render(have, "vlan", False))
                self.commands.append("exit")

    def _compare_config(self, wantd, haved):
        for hk, have in iteritems(haved):
            if hk not in wantd:
                self.commands.append(self._tmplt.render(have, "vlan", True))
        for wk, want in iteritems(wantd):
            have = haved.get(wk) or {}
            begin = len(self.commands)
            for x in self.dict_parsers:
                wx = get_from_dict(want, x) or {}
                hx = get_from_dict(have, x) or {}
                self._compare_dict(wx, hx, x)
            self.compare(parsers=self.linear_parsers, want=want, have=have)
            self._compare_dual(want, have)
            self._compare_mdns(want, have)
            if len(self.commands) != begin:
                self.commands.insert(begin, self._tmplt.render(want, "vlan", False))
                self.commands.append("exit")

    def _compare_dual(self, want, have):
        for x in self.dual_parsers:
            wx = get_from_dict(want, x) or {}
            hx = get_from_dict(have, x) or {}
            if wx == hx: continue
            if wx and wx["enable"]:
                self.compare(parsers=[x+".enable"], want=want, have={})
            else:
                self.compare(parsers=[x+".enable"], want=want, have=have)

    def _compare_mdns(self, want, have):
        mdns_len = len(self.commands)
        self.compare(parsers=["mdns_sd_gateway.enable"], want=want, have=have)
        if mdns_len == len(self.commands):
            if "mdns_sd_gateway" in want and want["mdns_sd_gateway"]["enable"]:
                mdns_len = len(self.commands)
                self.compare(parsers=self.mdns_parsers, want=want, have=have)
                if mdns_len != len(self.commands):
                    self.commands.insert(mdns_len, self._tmplt.render(want, "mdns_sd_gateway.enable", False))
                    self.commands.append("exit")
        elif "mdns_sd_gateway" in want and want["mdns_sd_gateway"]["enable"]:
                self.compare(parsers=self.mdns_parsers, want=want, have=have)
                self.commands.append("exit")

    def _compare_dict(self, want, have, x):
        have_remove = list(set(have.keys()).difference(set(want.keys())))
        for each in have_remove:
           hx_comp = self._construct_dict(x, have[each])
           self.compare(parsers=[x], want={}, have=hx_comp)
        for wk, wx in iteritems(want):
            hx = get_from_dict(have, wk) or {}
            wx_comp = self._construct_dict(x, wx)
            hx_comp = self._construct_dict(x, hx)
            self.compare(parsers=[x], want=wx_comp, have=hx_comp)

    def _construct_dict(self, vector, value):
        keys = vector.split(".")
        res = {}; a = res
        for key in keys:
            a.update({key:{}})
            a = a.get(key)
        a.update(value)
        return res

    def _list_to_dict(self, entry):
        for x in entry: # vlan config
            for k, val in iteritems(x): # member in k
                if k == "member":
                    if "pseudowire" in val and isinstance(val["pseudowire"], list):
                        val["pseudowire"] = {i["pwnumber"]: i for i in val["pseudowire"]}
                    if "ip_peer" in val  and isinstance(val["ip_peer"], list):
                        val["ip_peer"] = {(i["address"]+"_"+i["vc_id"]).replace(".","_"): i for i in val["ip_peer"]}
        entry = {x["vlan"]: x for x in entry}
        return entry