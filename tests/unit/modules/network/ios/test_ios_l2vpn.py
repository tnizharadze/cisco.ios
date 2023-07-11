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

    def test_l2vpn_gathered(self):
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
            "logging": {
                "pseudowire_status": True,
                "redundancy": True,
                "vc_state": True,
            },
            "redundancy_predictive_enabled": True,
            "pseudowire_group_status": True,
            "router_id": "4.4.4.4",
            "shutdown": True,
        }
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_l2vpn_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
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
                ),
                state="parsed",
            ),
        )

        parsed = {
            "logging": {
                "pseudowire_status": True,
                "redundancy": True,
                "vc_state": True,
            },
            "redundancy_predictive_enabled": True,
            "pseudowire_group_status": True,
            "router_id": "4.4.4.4",
            "shutdown": True,
        }

        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)


    def test_ios_l2vpn_rendered(self):
        set_module_args(
            dict(
                config={
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
                state="rendered",
            ),
        )
        commands = [
            "l2vpn",
            "logging pseudowire status",
            "logging redundancy",
            "logging vc-state",
            "redundancy predictive enabled",
            "pseudowire group status",
            "router-id 4.4.4.4",
            "shutdown",
            "exit",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(set(result["rendered"]), set(commands))

    def test_ios_l2vpn_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn
             logging pseudowire status
             logging redundancy
             redundancy predictive enabled
             router-id 5.5.5.5
            """,
        )
        set_module_args(
            dict(
                config={
                    "logging": {
                        "redundancy": False,
                        "vc_state": True,
                    },
                    "redundancy_predictive_enabled": True,
                    "pseudowire_group_status": False,
                    "router_id": "4.4.4.4",
                    "shutdown": True,
                },
                state="merged",
            ),
        )
        commands = [
            "l2vpn",
            "no logging redundancy",
            "logging vc-state",
            "router-id 4.4.4.4",
            "shutdown",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_ios_l2vpn_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn
             logging pseudowire status
             logging redundancy
             redundancy predictive enabled
             router-id 4.4.4.4
            """,
        )
        set_module_args(
            dict(
                config={
                    "logging": {
                        "redundancy": False,
                        "vc_state": True,
                    },
                    "redundancy_predictive_enabled": True,
                    "pseudowire_group_status": False,
                    "router_id": "4.4.4.4",
                    "shutdown": True,
                },
                state="replaced",
            ),
        )
        commands = [
            "l2vpn",
            "no logging pseudowire status",
            "no logging redundancy",
            "logging vc-state",
            "shutdown",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))


    def test_ios_l2vpn_deleted_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn
             logging pseudowire status
             logging redundancy
             logging vc-state
             redundancy predictive enabled
             router-id 4.4.4.4
             shutdown
            """,
        )
        set_module_args(
            dict(
                config={
                    "logging": {
                        "redundancy": False,
                        "vc_state": True,
                    },
                    "redundancy_predictive_enabled": True,
                    "pseudowire_group_status": False,
                    "router_id": "4.4.4.4",
                    "shutdown": True,
                },
                state="deleted",
            ),
        )
        commands = [
            "l2vpn",
            "no router-id 4.4.4.4",
            "no redundancy predictive enabled",
            "no shutdown",
            "no logging vc-state",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
