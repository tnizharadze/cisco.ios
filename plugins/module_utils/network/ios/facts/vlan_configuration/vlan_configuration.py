# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The ios vlan_configuration fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.vlan_configuration import (
    Vlan_configurationTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vlan_configuration.vlan_configuration import (
    Vlan_configurationArgs,
)


class Vlan_configurationFacts(object):
    """ The ios vlan_configuration facts class
    """

    def __init__(self, module, subspec='config', options='options'):
        self._module = module
        self.argument_spec = Vlan_configurationArgs.argument_spec

    def get_vlan_configuration_data(self, connection):
        return connection.get("show running-config | section ^vlan configuration")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Vlan_configuration network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_vlan_configuration_data(connection)

        # parse native config using the Vlan_configuration template
        vlan_configuration_parser = Vlan_configurationTemplate(lines=data.splitlines(), module=self._module)

        objs = vlan_configuration_parser.parse()
        for k, val in iteritems(objs):
            if "member" in val:
                if "pseudowire" in val["member"]:
                    val["member"]["pseudowire"] = list(val["member"]["pseudowire"].values())
                if "ip_peer" in val["member"]:
                    val["member"]["ip_peer"] = list(val["member"]["ip_peer"].values())
        objs = list(objs.values())

        params = utils.remove_empties(
            vlan_configuration_parser.validate_config(self.argument_spec, {"config": objs}, redact=True)
        )

        facts['vlan_configuration'] = params['config'] if 'config' in params else {}

        ansible_facts['ansible_network_resources'].pop('vlan_configuration', None)
        ansible_facts['ansible_network_resources'].update(facts)

        return ansible_facts
