# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The ios l2vpn_evpn fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.l2vpn_evpn import (
    L2vpn_evpnTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.l2vpn_evpn.l2vpn_evpn import (
    L2vpn_evpnArgs,
)

class L2vpn_evpnFacts(object):
    """ The ios l2vpn_evpn facts class
    """

    def __init__(self, module, subspec='config', options='options'):
        self._module = module
        self.argument_spec = L2vpn_evpnArgs.argument_spec

    def get_l2vpn_evpn_data(self, connection):
        return connection.get("show running-config | section ^l2vpn evpn$")


    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for L2vpn_evpn network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_l2vpn_evpn_data(connection)

        # parse native config using the L2vpn_evpn template
        l2vpn_evpn_parser = L2vpn_evpnTemplate(lines=data.splitlines(), module=self._module)

        objs = l2vpn_evpn_parser.parse()

        params = utils.remove_empties(
            l2vpn_evpn_parser.validate_config(self.argument_spec, {"config": objs}, redact=True)
        )

        facts['l2vpn_evpn'] = params['config'] if 'config' in params else {}

        ansible_facts['ansible_network_resources'].pop('l2vpn_evpn', None)
        ansible_facts['ansible_network_resources'].update(facts)

        return ansible_facts
