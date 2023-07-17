#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The ios_l2vpn_evpn_vb config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.l2vpn_evpn_vb import (
    L2vpn_evpn_vbTemplate,
)


class L2vpn_evpn_vb(ResourceModule):
    """
    The ios_l2vpn_evpn_vb config class
    """

    def __init__(self, module):
        super(L2vpn_evpn_vb, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="l2vpn_evpn_vb",
            tmplt=L2vpn_evpn_vbTemplate(),
        )
        self.linear_parsers = [
            "encapsulation",
            "rd",
            "auto_route_target",
            "replication_type",
            "ip_local_learning",
            "default_gateway_advertise",
            "multicast_advertise",
            "re_originate_route_type5",
        ]
        self.complex_parsers = [
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

        if self.state == "deleted":
            for k, hx in iteritems(deepcopy(haved)):
                if k in wantd and self._compare_for_delete(want=wantd[k], have=hx):
                    self.commands.append(self._tmplt.render(hx, "instance", True))
                    wantd.pop(k)
                    haved.pop(k)
            haved = self._dict_copy_deleted(wantd, haved)
            wantd = {}

        if self.state == "replaced":
            for k, hx in iteritems(deepcopy(haved)):
                if k not in wantd:
                    self.commands.append(self._tmplt.render(hx, "instance", True))
                    haved.pop(k)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        if wantd:
            for k, wx in iteritems(wantd):
                self._compare_entries(want=wx, have=haved.pop(k, {}))
        elif haved:
            for k, hx in iteritems(haved):
                self._compare_entries(want={}, have=hx)

    def _compare_entries(self, want, have):
        begin = len(self.commands)
        self._compare_lists(want, have)
        self.compare(parsers=self.linear_parsers, want=want, have=have)
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "instance", False))
            self.commands.append("exit")

    def _compare_lists(self, want, have):
        for x in self.complex_parsers:
            wx = set(get_from_dict(want, x) or [])
            hx = set(get_from_dict(have, x) or [])
            wdiff = sorted(list(wx - hx))
            hdiff = sorted(list(hx - wx))
            for each in hdiff:
                self.commands.append(self._tmplt.render({x: each}, x, True))
            for each in wdiff:
                self.commands.append(self._tmplt.render({x: each}, x, False))

    def _dict_copy_deleted(self, want, have, x=""):
        hrec = {}
        have_dict = have if x == "" else get_from_dict(have, x)
        for k, hx in iteritems(have_dict):
            if not want:
                hrec.update({k: hx})
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
            elif wx == hx:
                hrec.update({k: hx})
        return hrec

    def _compare_for_delete(self, want, have):
        result = True
        for k, hx in iteritems(have):
            if k in want and hx == want[k]:
                continue
            else:
                result = False
                break
        return result

    def _l2vpn_list_to_dict(self, entry):
        for x in entry:
            for k, val in iteritems(x):
                if isinstance(val, list):
                    x[k] = sorted(val)
        entry = {x["instance"]: x for x in entry}
        return entry
