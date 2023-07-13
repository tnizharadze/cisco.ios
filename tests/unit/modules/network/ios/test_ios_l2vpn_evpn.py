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

from ansible_collections.cisco.ios.plugins.modules import ios_l2vpn_evpn
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule

class TestIosL2VPNEVPNModule(TestIosModule):
    module = ios_l2vpn_evpn

    def setUp(self):
        super(TestIosL2VPNEVPNModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.l2vpn_evpn.l2vpn_evpn."
            "L2vpn_evpnFacts.get_l2vpn_evpn_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()
        self.maxDiff = None

    def tearDown(self):
        super(TestIosL2VPNEVPNModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_l2vpn_evpn_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn
             logging vpws vc-state
             logging peer state
             replication-type static
             flooding-suppression address-resolution disable
             ip duplication limit 234 time 234
             mac duplication limit 213 time 123
             router-id Loopback0
             multihoming aliasing disable
             ip local-learning disable
             ip local-learning limit per-mac ipv4 345
             ip local-learning limit per-mac ipv6 2345
             ip local-learning time down 234
             ip local-learning time poll 223
             ip local-learning time reachable 234
             ip local-learning time stale 23
             default-gateway advertise
             route-target auto vni
             multicast advertise
            """,
        )
        gathered = {
            "logging": {
                "peer_state": True,
                "vpws_vc_state": True,
            },
            "replication_type": "static",
            "flooding_suppression_address_resolution_disable": True, 
            "ip_duplication": {
                "limit": 234,
                "time": 234,
            },
            "mac_duplication": {
                "limit": 213,
                "time": 123,
            },
            "router_id": "Loopback0",
            "multihoming_aliasing_disable": True,
            "ip_local_learning": {
                "disable": True,
                "limit_per_mac_ipv4": 345,
                "limit_per_mac_ipv6": 2345,
                "time": {
                    "down": 234,
                    "poll": 223,
                    "reachable": 234,
                    "stale": 23,
                },
            },
            "default_gateway_advertise": True,
            "route_target_auto_vni": True,
            "multicast_advertise": True,
        }
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_ios_l2vpn_evpn_rendered(self):
        set_module_args(
            dict(
                config={
                    "logging": {
                        "peer_state": True,
                        "vpws_vc_state": True,
                    },
                    "replication_type": "static",
                    "flooding_suppression_address_resolution_disable": True, 
                    "ip_duplication": {
                        "limit": 234,
                        "time": 234,
                    },
                    "mac_duplication": {
                        "limit": 213,
                        "time": 123,
                    },
                    "router_id": "Loopback0",
                    "multihoming_aliasing_disable": True,
                    "ip_local_learning": {
                        "disable": True,
                        "limit_per_mac_ipv4": 345,
                        "limit_per_mac_ipv6": 2345,
                        "time": {
                            "down": 234,
                            "poll": 223,
                            "reachable": 234,
                            "stale": 23,
                        },
                    },
                    "default_gateway_advertise": True,
                    "route_target_auto_vni": True,
                    "multicast_advertise": True,
                },
                state="rendered",
            ),
        )
        commands = [
            "l2vpn evpn",
            "logging vpws vc-state",
            "logging peer state",
            "replication-type static",
            "flooding-suppression address-resolution disable",
            "ip duplication limit 234 time 234",
            "mac duplication limit 213 time 123",
            "router-id Loopback0",
            "multihoming aliasing disable",
            "ip local-learning disable",
            "ip local-learning limit per-mac ipv4 345",
            "ip local-learning limit per-mac ipv6 2345",
            "ip local-learning time down 234",
            "ip local-learning time poll 223",
            "ip local-learning time reachable 234",
            "ip local-learning time stale 23",
            "default-gateway advertise",
            "route-target auto vni",
            "multicast advertise",
            "exit",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(set(result["rendered"]), set(commands))

    def test_ios_l2vpn_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn
             logging vpws vc-state
             logging peer state
             replication-type static
             flooding-suppression address-resolution disable
             ip duplication limit 234 time 234
             mac duplication limit 213 time 123
             router-id Loopback0
             multihoming aliasing disable
             ip local-learning disable
             ip local-learning limit per-mac ipv4 345
             ip local-learning limit per-mac ipv6 2345
             default-gateway advertise
             route-target auto vni
             multicast advertise
            """,
        )
        set_module_args(
            dict(
                config={
                    "logging": {
                        "peer_state": True,
                        "vpws_vc_state": True,
                    },
                    "replication_type": "static",
                    "flooding_suppression_address_resolution_disable": True, 
                    "ip_duplication": {
                        "limit": 234,
                        "time": 234,
                    },
                    "mac_duplication": {
                        "limit": 213,
                        "time": 123,
                    },
                    "router_id": "Loopback0",
                    "multihoming_aliasing_disable": True,
                    "ip_local_learning": {
                        "disable": True,
                        "limit_per_mac_ipv4": 345,
                        "limit_per_mac_ipv6": 2345,
                        "time": {
                            "down": 234,
                            "poll": 223,
                            "reachable": 234,
                            "stale": 23,
                        },
                    },
                    "default_gateway_advertise": True,
                    "route_target_auto_vni": True,
                    "multicast_advertise": True,
                },
                state="merged",
            ),
        )
        commands = [
            "l2vpn evpn",
            "ip local-learning time down 234",
            "ip local-learning time poll 223",
            "ip local-learning time reachable 234",
            "ip local-learning time stale 23",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_ios_l2vpn_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn
             logging vpws vc-state
             logging peer state
             replication-type static
             flooding-suppression address-resolution disable
             ip duplication limit 234 time 234
             mac duplication limit 213 time 123
             router-id Loopback0
             multihoming aliasing disable
             ip local-learning disable
             ip local-learning limit per-mac ipv4 345
             ip local-learning limit per-mac ipv6 2345
             ip local-learning time down 234
             ip local-learning time poll 223
             ip local-learning time reachable 234
             ip local-learning time stale 23
             default-gateway advertise
             route-target auto vni
             multicast advertise
            """,
        )
        set_module_args(
            dict(
                config={
                    "logging": {
                        "peer_state": False,
                        "vpws_vc_state": False,
                    },
                    "replication_type": "static",
                    "flooding_suppression_address_resolution_disable": True, 
                    "ip_duplication": {
                        "limit": 234,
                        "time": 234,
                    },
                    "router_id": "Loopback0",
                    "default_gateway_advertise": True,
                    "route_target_auto_vni": True,
                    "multicast_advertise": True,
                },
                state="replaced",
            ),
        )
        commands = [
            "l2vpn evpn",
            "no logging vpws vc-state",
            "no logging peer state",
            "no ip local-learning time reachable 234",
            "no mac duplication limit 213 time 123",
            "no ip local-learning disable",
            "no ip local-learning limit per-mac ipv4 345",
            "no ip local-learning limit per-mac ipv6 2345",
            "no ip local-learning time down 234",
            "no ip local-learning time stale 23",
            "no ip local-learning time poll 223",
            "no multihoming aliasing disable",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))


    def test_ios_l2vpn_deleted_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn
             logging vpws vc-state
             logging peer state
             replication-type static
             flooding-suppression address-resolution disable
             ip duplication limit 234 time 234
             mac duplication limit 213 time 123
             router-id Loopback0
             multihoming aliasing disable
             ip local-learning disable
             ip local-learning limit per-mac ipv4 345
             ip local-learning limit per-mac ipv6 2345
             ip local-learning time down 234
             ip local-learning time poll 223
             ip local-learning time reachable 234
             ip local-learning time stale 23
             default-gateway advertise
             route-target auto vni
             multicast advertise
            """,
        )
        set_module_args(
            dict(
                config={
                    "logging": {
                        "vpws_vc_state": False,
                    },
                    "replication_type": "static",
                    "mac_duplication": {
                        "limit": 213,
                        "time": 123,
                    },
                },
                state="deleted",
            ),
        )
        commands = [
            "l2vpn evpn",
            "no mac duplication limit 213 time 123",
            "no replication-type static",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
