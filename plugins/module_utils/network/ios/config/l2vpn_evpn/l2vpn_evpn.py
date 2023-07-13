#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The ios_l2vpn_evpn config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.l2vpn_evpn import (
    L2vpn_evpnTemplate,
)


class L2vpn_evpn(ResourceModule):
    """
    The ios_l2vpn_evpn config class
    """

    def __init__(self, module):
        super(L2vpn_evpn, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="l2vpn_evpn",
            tmplt=L2vpn_evpnTemplate(),
        )
        self.linear_parsers  = [
            "logging.peer_state",
            "logging.vpws_vc_state",
            "replication_type",
            "flooding_suppression_address_resolution_disable",
            "ip_duplication",
            "mac_duplication",
            "router_id",
            "multihoming_aliasing_disable",
            "ip_local_learning.disable",
            "ip_local_learning.limit_per_mac_ipv4",
            "ip_local_learning.limit_per_mac_ipv6",
            "ip_local_learning.time.down",
            "ip_local_learning.time.poll",
            "ip_local_learning.time.reachable",
            "ip_local_learning.time.stale",
            "default_gateway_advertise",
            "route_target_auto_vni",
            "multicast_advertise",
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
        wantd = {k: v for k, v in iteritems(self.want) }
        haved = {k: v for k, v in iteritems(self.have) }

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = self._dict_copy_deleted(want=wantd, have=haved)
            wantd = {}

        self._compare_linear(wantd, haved)

    def _compare_linear(self, want, have):
        cmd_len = len(self.commands)
        for x in self.linear_parsers:
            self.compare([x], want=want, have=have)
        if cmd_len < len(self.commands):
            self.commands.insert(cmd_len,"l2vpn evpn")
            self.commands.append("exit")

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
            elif wx == hx:
                hrec.update({k: hx})
        return hrec
