# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent

from ansible_collections.cisco.ios.plugins.modules import ios_l2vpn
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosL2VPNModule(TestIosModule):
    module = ios_l2vpn

    def setUp(self):
        super(TestIosL2VPNModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.l2vpn.l2vpn."
            "L2vpnFacts.get_l2vpn_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosL2VPNModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_ios_spanning_tree_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn
             logging pseudowire status
             logging redundancy
             logging vc-state
             redundancy predictive enabled
             pseudowire group status
             router-id 4.4.4.4
             shutdown
            """,
        )
        gathered = {
            "l2vpn": {
                "logging": {
                    "pseudowire_status": True,
                    "redundancy": True,
                    "vc_state": True,
                },
                "redundancy_predictive_enabled": True,
                "pseudowire_group_status": True,
                "router_id": "4.4.4.4",
                "shutdown": True,
            },
        }
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)
