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

from ansible_collections.cisco.ios.plugins.modules import ios_vlan_configuration
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosVLANCONFIGModule(TestIosModule):
    module = ios_vlan_configuration

    def setUp(self):
        super(TestIosVLANCONFIGModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.vlan_configuration.vlan_configuration."
            "Vlan_configurationFacts.get_vlan_configuration_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()
        self.maxDiff = None

    def tearDown(self):
        super(TestIosVLANCONFIGModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_vlan_configuration_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            vlan configuration 10
             member access-vfi OVERLAY
             member pseudowire100
             member pseudowire35 2.2.3.3 123 encapsulation mpls
             member 10.10.10.10 123 encapsulation mpls
             member 3.4.5.6 123 encapsulation mpls
             member 5.3.2.1 123 template DVFR
             member 5.5.5.5 444 template sdsd
             member 5.5.5.5 123 encapsulation mpls
             member 4.4.4.4 123 template RR
             member 4.4.4.4 345 encapsulation mpls
             member 4.4.4.4 14342 template TEST
             member 4.4.4.4 423 encapsulation mpls
             member pseudowire34 23.23.23.23 123 encapsulation mpls
             member pseudowire23542 5.5.5.5 342 template BFD
             member pseudowire23423
             member vni 6060
             device-tracking attach-policy example_policy
             mdns-sd gateway
              active-query timer 44
              transport both
              service-inst-suffix TEST2
              service-mdns-query ptr
              source-interface GigabitEthernet1/0/1
              sdg-agent 6.6.6.6
              service-policy TEST_POL
            vlan configuration 11
             member vfi VPLSVFI
             member pseudowire36
             member pseudowire101 4.5.6.7 333 template TETE
             et-analytics enable
             ipv6 destination-guard
             ipv6 dhcp guard attach-policy TEST2
             ipv6 nd ra-throttler
             ipv6 nd raguard attach-policy TEST
             ipv6 nd suppress
            vlan configuration 12
             member evpn-instance 354 vni 500100 protected
             mdns-sd gateway
             ipv6 destination-guard attach-policy TEST
             ipv6 dhcp ldra attach-policy client-facing-untrusted
             ipv6 dhcp guard
             ipv6 nd ra-throttler attach-policy TEST2
             ipv6 nd raguard
             ipv6 nd suppress attach-policy TEST
           """,
        )
        gathered = [
            {
                "vlan": "10",
                "member": {
                    "access_vfi": "OVERLAY",
                    "vni": "6060",
                    "pseudowire": [
                        {"pwnumber": "100"},
                        {"pwnumber": "35", "address": "2.2.3.3", "vc_id": "123"},
                        {"pwnumber": "34", "address": "23.23.23.23", "vc_id": "123"},
                        {"pwnumber": "23542", "address": "5.5.5.5", "vc_id": "342", "template": "BFD"},
                        {"pwnumber": "23423"},
                    ],
                    "ip_peer": [
                        {"address": "10.10.10.10", "vc_id": "123"},
                        {"address": "3.4.5.6", "vc_id": "123"},
                        {"address": "5.3.2.1", "vc_id": "123", "template": "DVFR"},
                        {"address": "5.5.5.5", "vc_id": "444", "template": "sdsd"},
                        {"address": "5.5.5.5", "vc_id": "123"},
                        {"address": "4.4.4.4", "vc_id": "123", "template": "RR"},
                        {"address": "4.4.4.4", "vc_id": "345"},
                        {"address": "4.4.4.4", "vc_id": "14342", "template": "TEST"},
                        {"address": "4.4.4.4", "vc_id": "423"},
                    ],
                },
                "mdns_sd_gateway": {
                    "enable": True,
                    "active_query_timer": "44",
                    "sdg_agent": "6.6.6.6",
                    "service_inst_suffix": "TEST2",
                    "service_mdns_query": "ptr",
                    "service_policy": "TEST_POL",
                    "source_interface": "GigabitEthernet1/0/1",
                    "transport": "both",
                },
                "device_tracking": {
                    "enable": True,
                    "attach_policy": "example_policy",
                },
            },
            {
                "vlan": "11",
                "member": {
                    "vfi": "VPLSVFI",
                    "pseudowire": [
                        {"pwnumber": "36"},
                        {"pwnumber": "101", "address": "4.5.6.7", "vc_id": "333", "template": "TETE"},
                    ],
                },
                "et_analytics_enable": True,
                "ipv6": {
                    "destination_guard": {
                        "enable": True,
                    },
                    "dhcp": {
                        "guard": {"enable": True, "attach_policy": "TEST2"},
                    },
                    "nd": {
                        "ra_throttler": {"enable": True},
                        "raguard": {"enable": True, "attach_policy": "TEST"},
                        "suppress": {"enable": True},
                    },
                },
            },
            {
                "vlan": "12",
                "member": {
                    "evpn": {
                        "instance": "354",
                        "vni": "500100",
                        "protected": True,
                    },
                },
                "mdns_sd_gateway": {
                    "enable": True,
                },
                "ipv6": {
                    "destination_guard": {
                        "enable": True,
                        "attach_policy": "TEST",
                    },
                    "dhcp": {
                        "guard": {"enable": True},
                        "ldra_attach_policy": "client-facing-untrusted",
                    },
                    "nd": {
                        "ra_throttler": {"enable": True, "attach_policy": "TEST2"},
                        "raguard": {"enable": True},
                        "suppress": {"enable": True, "attach_policy": "TEST"},
                    },
                },
            },
        ]
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_ios_vlan_configuration_rendered(self):
        set_module_args(
            dict(
                config=[
                    {
                        "vlan": "10",
                        "member": {
                            "access_vfi": "OVERLAY",
                            "vni": "6060",
                            "pseudowire": [
                                {"pwnumber": "100"},
                                {"pwnumber": "35", "address": "2.2.3.3", "vc_id": "123"},
                                {"pwnumber": "34", "address": "23.23.23.23", "vc_id": "123"},
                                {"pwnumber": "23542", "address": "5.5.5.5", "vc_id": "342", "template": "BFD"},
                                {"pwnumber": "23423"},
                            ],
                            "ip_peer": [
                                {"address": "10.10.10.10", "vc_id": "123"},
                                {"address": "3.4.5.6", "vc_id": "123"},
                                {"address": "5.3.2.1", "template": "DVFR", "vc_id": "123"},
                                {"address": "5.5.5.5", "template": "sdsd", "vc_id": "123"},
                                {"address": "4.4.4.4", "template": "TEST", "vc_id": "423"},
                            ],
                        },
                        "mdns_sd_gateway": {
                            "enable": True,
                            "active_query_timer": "44",
                            "sdg_agent": "6.6.6.6",
                            "service_inst_suffix": "TEST2",
                            "service_mdns_query": "ptr",
                            "service_policy": "TEST_POL",
                            "source_interface": "GigabitEthernet1/0/1",
                            "transport": "both",
                        },
                        "device_tracking": {
                            "enable": True,
                            "attach_policy": "example_policy",
                        },
                    },
                    {
                        "vlan": "11",
                        "member": {
                            "vfi": "VPLSVFI",
                            "pseudowire": [
                                {"pwnumber": "36"},
                                {"pwnumber": "101", "address": "4.5.6.7", "vc_id": "333", "template": "TETE"},
                            ],
                        },
                        "et_analytics_enable": True,
                        "ipv6": {
                            "destination_guard": {
                                "enable": True,
                            },
                            "dhcp": {
                                "guard": {"enable": True, "attach_policy": "TEST2"},
                            },
                            "nd": {
                                "ra_throttler": {"enable": True},
                                "raguard": {"enable": True, "attach_policy": "TEST"},
                                "suppress": {"enable": True},
                            },
                        },
                    },
                    {
                        "vlan": "12",
                        "member": {
                            "evpn": {
                                "instance": "354",
                                "vni": "500100",
                                "protected": True,
                            },
                        },
                        "mdns_sd_gateway": {
                            "enable": True,
                        },
                        "ipv6": {
                            "destination_guard": {
                                "enable": True,
                                "attach_policy": "TEST",
                            },
                            "dhcp": {
                                "guard": {"enable": True},
                                "ldra_attach_policy": "client-facing-untrusted",
                            },
                            "nd": {
                                "ra_throttler": {"enable": True, "attach_policy": "TEST2"},
                                "raguard": {"enable": True},
                                "suppress": {"enable": True, "attach_policy": "TEST"},
                            },
                        },
                    },
                ],
                state="rendered",
            ),
        )
        commands = [
            "vlan configuration 10",
            "member access-vfi OVERLAY",
            "member pseudowire100",
            "member pseudowire35 2.2.3.3 123 encapsulation mpls",
            "member 10.10.10.10 123 encapsulation mpls",
            "member 3.4.5.6 123 encapsulation mpls",
            "member 5.3.2.1 123 template DVFR",
            "member 5.5.5.5 123 template sdsd",
            "member 4.4.4.4 423 template TEST",
            "member pseudowire34 23.23.23.23 123 encapsulation mpls",
            "member pseudowire23542 5.5.5.5 342 template BFD",
            "member pseudowire23423",
            "member vni 6060",
            "device-tracking attach-policy example_policy",
            "mdns-sd gateway",
            "active-query timer 44",
            "transport both",
            "service-inst-suffix TEST2",
            "service-mdns-query ptr",
            "source-interface GigabitEthernet1/0/1",
            "sdg-agent 6.6.6.6",
            "service-policy TEST_POL",
            "exit",
            "exit",
            "vlan configuration 11",
            "member vfi VPLSVFI",
            "member pseudowire36",
            "member pseudowire101 4.5.6.7 333 template TETE",
            "et-analytics enable",
            "ipv6 destination-guard",
            "ipv6 dhcp guard attach-policy TEST2",
            "ipv6 nd ra-throttler",
            "ipv6 nd raguard attach-policy TEST",
            "ipv6 nd suppress",
            "exit",
            "vlan configuration 12",
            "member evpn-instance 354 vni 500100 protected",
            "mdns-sd gateway",
            "exit",
            "ipv6 destination-guard attach-policy TEST",
            "ipv6 dhcp ldra attach-policy client-facing-untrusted",
            "ipv6 dhcp guard",
            "ipv6 nd ra-throttler attach-policy TEST2",
            "ipv6 nd raguard",
            "ipv6 nd suppress attach-policy TEST",
            "exit",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_vlan_configuration_deleted_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            vlan configuration 10
             member access-vfi OVERLAY
             member pseudowire100
             member pseudowire35 2.2.3.3 123 encapsulation mpls
             member 10.10.10.10 123 encapsulation mpls
             member 3.4.5.6 123 encapsulation mpls
             member 5.3.2.1 123 template DVFR
             member 5.5.5.5 444 template sdsd
             member 5.5.5.5 123 encapsulation mpls
             member 4.4.4.4 123 template RR
             member pseudowire34 23.23.23.23 123 encapsulation mpls
             member pseudowire23542 5.5.5.5 342 template BFD
             member pseudowire23423
             member 4.4.4.4 345 encapsulation mpls
             member 4.4.4.4 14342 template TEST
             member 4.4.4.4 423 encapsulation mpls
             member vni 6060
             device-tracking attach-policy example_policy
             mdns-sd gateway
              active-query timer 44
              transport both
              service-inst-suffix TEST2
              service-mdns-query ptr
              source-interface GigabitEthernet1/0/1
              sdg-agent 6.6.6.6
              service-policy TEST_POL
            vlan configuration 11
             member vfi VPLSVFI
             member pseudowire36
             member pseudowire101 4.5.6.7 333 template TETE
             et-analytics enable
             ipv6 destination-guard
             ipv6 dhcp guard attach-policy TEST2
             ipv6 nd ra-throttler
             ipv6 nd raguard attach-policy TEST
             ipv6 nd suppress
            vlan configuration 12
             member evpn-instance 354 vni 500100 protected
             mdns-sd gateway
             ipv6 destination-guard attach-policy TEST
             ipv6 dhcp ldra attach-policy client-facing-untrusted
             ipv6 dhcp guard
             ipv6 nd ra-throttler attach-policy TEST2
             ipv6 nd raguard
             ipv6 nd suppress attach-policy TEST
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "vlan": "10",
                        "member": {
                            "vni": "6060",
                            "pseudowire": [
                                {"pwnumber": "100"},
                                {"pwnumber": "35", "address": "2.2.3.3", "vc_id": "123"},
                                {"pwnumber": "34", "address": "23.23.23.23", "vc_id": "123"},
                                {"pwnumber": "23542", "address": "5.5.5.5", "vc_id": "342", "template": "BFD"},
                            ],
                            "ip_peer": [
                                {"address": "10.10.10.10", "vc_id": "123"},
                                {"address": "3.4.5.6", "vc_id": "123"},
                                {"address": "5.3.2.1", "template": "DVFR", "vc_id": "123"},
                                {"address": "5.5.5.5", "template": "sdsd", "vc_id": "123"},
                                {"address": "4.4.4.4", "vc_id": "123", "template": "RR"},
                                {"address": "4.4.4.4", "vc_id": "423"},
                            ],
                        },
                        "mdns_sd_gateway": {
                            "enable": True,
                            "active_query_timer": "44",
                            "sdg_agent": "6.6.6.6",
                            "service_mdns_query": "ptr",
                            "service_policy": "TEST_POL",
                            "transport": "both",
                        },
                        "device_tracking": {
                            "enable": True,
                            "attach_policy": "example_policy",
                        },
                    },
                    {
                        "vlan": "12",
                        "member": {
                            "evpn": {
                                "instance": "354",
                                "vni": "500100",
                                "protected": True,
                            },
                        },
                        "mdns_sd_gateway": {
                            "enable": True,
                        },
                        "ipv6": {
                            "destination_guard": {
                                "enable": True,
                                "attach_policy": "TEST",
                            },
                            "dhcp": {
                                "guard": {"enable": True},
                                "ldra_attach_policy": "client-facing-untrusted",
                            },
                            "nd": {
                                "ra_throttler": {"enable": True, "attach_policy": "TEST2"},
                                "raguard": {"enable": True},
                                "suppress": {"enable": True, "attach_policy": "TEST"},
                            },
                        },
                    },
                ],
                state="deleted",
            ),
        )
        commands = [
            "vlan configuration 10",
            "no member vni 6060",
            "no member pseudowire100",
            "no member pseudowire35 2.2.3.3 123 encapsulation mpls",
            "no member pseudowire34 23.23.23.23 123 encapsulation mpls",
            "no member pseudowire23542 5.5.5.5 342 template BFD",
            "no member 10.10.10.10 123 encapsulation mpls",
            "no member 3.4.5.6 123 encapsulation mpls",
            "no member 5.3.2.1 123 template DVFR",
            "no member 5.5.5.5 123 encapsulation mpls",
            "no member 4.4.4.4 123 template RR",
            "no member 4.4.4.4 423 encapsulation mpls",
            "no device-tracking attach-policy example_policy",
            "mdns-sd gateway",
            "no active-query timer 44",
            "no sdg-agent 6.6.6.6",
            "no service-mdns-query ptr",
            "no service-policy TEST_POL",
            "no transport both",
            "exit",
            "exit",
            "no vlan configuration 12",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vlan_configuration_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            vlan configuration 10
             member access-vfi OVERLAY
             member pseudowire100
             member pseudowire35 2.2.3.3 123 encapsulation mpls
             member 10.10.10.10 123 encapsulation mpls
             member 3.4.5.6 123 encapsulation mpls
             member 5.3.2.1 123 template DVFR
             member 5.5.5.5 444 template sdsd
             member 5.5.5.5 123 encapsulation mpls
             member 4.4.4.4 123 template RR
             member 4.4.4.4 345 encapsulation mpls
             member 4.4.4.4 14342 template TEST
             member 4.4.4.4 423 encapsulation mpls
             member pseudowire34 23.23.23.23 123 encapsulation mpls
             member pseudowire23542 5.5.5.5 342 template BFD
             member pseudowire23423
             member vni 6060
             device-tracking attach-policy example_policy
             mdns-sd gateway
              active-query timer 44
              transport both
              service-inst-suffix TEST2
              service-mdns-query ptr
              source-interface GigabitEthernet1/0/1
              sdg-agent 6.6.6.6
              service-policy TEST_POL
            vlan configuration 11
             member vfi VPLSVFI
             member pseudowire36
             member pseudowire101 4.5.6.7 333 template TETE
             et-analytics enable
             ipv6 destination-guard
             ipv6 dhcp guard attach-policy TEST2
             ipv6 nd ra-throttler
             ipv6 nd raguard attach-policy TEST
             ipv6 nd suppress
            vlan configuration 12
             member evpn-instance 354 vni 500100 protected
             mdns-sd gateway
             ipv6 destination-guard attach-policy TEST
             ipv6 dhcp ldra attach-policy client-facing-untrusted
             ipv6 dhcp guard
             ipv6 nd ra-throttler attach-policy TEST2
             ipv6 nd raguard
             ipv6 nd suppress attach-policy TEST
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "vlan": "10",
                        "member": {
                            "access_vfi": "OVERLAY",
                            "vni": "6060",
                            "pseudowire": [
                                {"pwnumber": "100"},
                                {"pwnumber": "34", "address": "23.23.23.23", "vc_id": "123"},
                                {"pwnumber": "23542", "address": "5.5.5.5", "vc_id": "342", "template": "BFD"},
                                {"pwnumber": "23423", "address": "2.2.3.3", "vc_id": "123", "template": "BFD"},
                            ],
                            "ip_peer": [
                                {"address": "10.10.10.10", "vc_id": "123"},
                                {"address": "3.4.5.6", "vc_id": "123"},
                                {"address": "5.3.2.1", "vc_id": "123"},
                                {"address": "5.5.5.5", "vc_id": "123", "template": "sdsd"},
                                {"address": "4.4.4.4", "vc_id": "123", "template": "RR"},
                                {"address": "4.4.4.4", "vc_id": "345"},
                                {"address": "4.4.4.4", "vc_id": "14342", "template": "TEST"},
                                {"address": "4.4.4.4", "vc_id": "423", "template": "TEST"},
                            ],
                        },
                        "mdns_sd_gateway": {
                            "enable": True,
                            "active_query_timer": "45",
                            "sdg_agent": "6.6.5.5",
                            "service_inst_suffix": "TEST3",
                            "service_mdns_query": "ptr",
                            "service_policy": "TEST_POL",
                            "source_interface": "GigabitEthernet1/0/1",
                        },
                        "device_tracking": {
                            "enable": False,
                            "attach_policy": "example_policy",
                        },
                    },
                    {
                        "vlan": "11",
                        "member": {
                            "vfi": "VPLSVFI",
                            "pseudowire": [
                                {"pwnumber": "36"},
                                {"pwnumber": "101", "address": "4.5.6.7", "vc_id": "333", "template": "TETE"},
                            ],
                        },
                        "et_analytics_enable": True,
                        "ipv6": {
                            "destination_guard": {
                                "enable": False,
                            },
                            "dhcp": {
                                "guard": {"enable": False, "attach_policy": "TEST"},
                            },
                            "nd": {
                                "ra_throttler": {"enable": True, "attach_policy": "TEST4"},
                                "raguard": {"enable": False, "attach_policy": "TEST"},
                                "suppress": {"enable": True},
                            },
                        },
                    },
                    {
                        "vlan": "12",
                        "member": {
                            "evpn": {
                                "instance": "354",
                                "vni": "500101",
                                "protected": True,
                            },
                        },
                        "mdns_sd_gateway": {
                            "enable": True,
                        },
                        "ipv6": {
                            "destination_guard": {
                                "enable": True,
                                "attach_policy": "TEST",
                            },
                            "dhcp": {
                                "guard": {"enable": True},
                                "ldra_attach_policy": "client-facing-untrusted",
                            },
                            "nd": {
                                "ra_throttler": {"enable": True, "attach_policy": "TEST2"},
                                "raguard": {"enable": True},
                                "suppress": {"enable": True, "attach_policy": "TEST"},
                            },
                        },
                    },
                ],
                state="replaced",
            ),
        )
        commands = [
            "vlan configuration 10",
            "no member pseudowire35 2.2.3.3 123 encapsulation mpls",
            "member pseudowire23423 2.2.3.3 123 template BFD",
            "member 4.4.4.4 423 template TEST",
            "member 5.3.2.1 123 encapsulation mpls",
            "member 5.5.5.5 123 template sdsd",
            "no member 5.5.5.5 444 template sdsd",
            "mdns-sd gateway",
            "active-query timer 45",
            "service-inst-suffix TEST3",
            "sdg-agent 6.6.5.5",
            "no transport both",
            "exit",
            "no device-tracking attach-policy example_policy",
            "exit",
            "vlan configuration 11",
            "no ipv6 nd raguard attach-policy TEST",
            "no ipv6 destination-guard",
            "no ipv6 dhcp guard attach-policy TEST2",
            "ipv6 nd ra-throttler attach-policy TEST4",
            "exit",
            "vlan configuration 12",
            "member evpn-instance 354 vni 500101 protected",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vlan_configuration_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            vlan configuration 10
             member access-vfi OVERLAY
             member pseudowire100
             member pseudowire35 2.2.3.3 123 encapsulation mpls
             member 10.10.10.10 123 encapsulation mpls
             member 3.4.5.6 123 encapsulation mpls
             member 5.3.2.1 123 template DVFR
             member 5.5.5.5 444 template sdsd
             member 5.5.5.5 123 encapsulation mpls
             member 4.4.4.4 123 template RR
             member pseudowire34 23.23.23.23 123 encapsulation mpls
             member pseudowire23542 5.5.5.5 342 template BFD
             member pseudowire23423
             member vni 6060
             device-tracking attach-policy example_policy
             mdns-sd gateway
              active-query timer 44
              transport both
              service-inst-suffix TEST2
              service-mdns-query ptr
              source-interface GigabitEthernet1/0/1
              sdg-agent 6.6.6.6
              service-policy TEST_POL
            vlan configuration 11
             member vfi VPLSVFI
             member pseudowire36
             member pseudowire101 4.5.6.7 333 template TETE
             et-analytics enable
             ipv6 destination-guard
             ipv6 dhcp guard attach-policy TEST2
             ipv6 nd ra-throttler
             ipv6 nd raguard attach-policy TEST
             ipv6 nd suppress
            vlan configuration 12
             member evpn-instance 354 vni 500100 protected
             mdns-sd gateway
             ipv6 destination-guard attach-policy TEST
             ipv6 dhcp ldra attach-policy client-facing-untrusted
             ipv6 dhcp guard
             ipv6 nd ra-throttler attach-policy TEST2
             ipv6 nd raguard
             ipv6 nd suppress attach-policy TEST
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "vlan": "10",
                        "member": {
                            "access_vfi": "OVERLAY",
                            "vni": "6060",
                            "pseudowire": [
                                {"pwnumber": "100"},
                                {"pwnumber": "35", "address": "2.2.3.3", "vc_id": "123"},
                                {"pwnumber": "34", "address": "23.23.23.23", "vc_id": "123"},
                                {"pwnumber": "23542", "address": "5.5.5.5", "vc_id": "342", "template": "BFD"},
                                {"pwnumber": "23423"},
                            ],
                            "ip_peer": [
                                {"address": "10.10.10.10", "vc_id": "123"},
                                {"address": "3.4.5.6", "vc_id": "123"},
                                {"address": "5.3.2.1", "vc_id": "123", "template": "DVFR"},
                                {"address": "5.5.5.5", "vc_id": "444", "template": "TEST3"},
                                {"address": "5.5.5.5", "vc_id": "123"},
                                {"address": "4.4.4.4", "vc_id": "123", "template": "RR"},
                                {"address": "4.4.4.4", "vc_id": "345"},
                                {"address": "4.4.4.4", "vc_id": "14342", "template": "TEST"},
                                {"address": "4.4.4.4", "vc_id": "423"},
                            ],
                        },
                        "device_tracking": {
                            "enable": False,
                        },
                    },
                    {
                        "vlan": "11",
                        "member": {
                            "vfi": "VPLSVFI",
                            "pseudowire": [
                                {"pwnumber": "36"},
                                {"pwnumber": "101", "address": "4.5.6.7", "vc_id": "333", "template": "TETE"},
                            ],
                        },
                        "et_analytics_enable": True,
                        "ipv6": {
                            "destination_guard": {
                                "enable": False,
                            },
                            "dhcp": {
                                "guard": {"enable": True, "attach_policy": "TEST2"},
                            },
                            "nd": {
                                "ra_throttler": {"enable": True},
                                "raguard": {"enable": True, "attach_policy": "TEST"},
                                "suppress": {"enable": True},
                            },
                        },
                    },
                    {
                        "vlan": "12",
                        "member": {
                            "evpn": {
                                "instance": "354",
                                "vni": "500100",
                                "protected": True,
                            },
                        },
                        "mdns_sd_gateway": {
                            "enable": True,
                        },
                        "ipv6": {
                            "destination_guard": {
                                "enable": True,
                                "attach_policy": "TEST",
                            },
                            "dhcp": {
                                "guard": {"enable": False},
                            },
                            "nd": {
                                "ra_throttler": {"enable": True, "attach_policy": "TEST2"},
                                "raguard": {"enable": True},
                                "suppress": {"enable": True, "attach_policy": "TEST"},
                            },
                        },
                    },
                ],
                state="merged",
            ),
        )
        commands = [
            "vlan configuration 10",
            "member 4.4.4.4 14342 template TEST",
            "member 4.4.4.4 345 encapsulation mpls",
            "member 4.4.4.4 423 encapsulation mpls",
            "member 5.5.5.5 444 template TEST3",
            "no device-tracking attach-policy example_policy",
            "exit",
            "vlan configuration 11",
            "no ipv6 destination-guard",
            "exit",
            "vlan configuration 12",
            "no ipv6 dhcp guard",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vlan_configuration_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    vlan configuration 10
                     member access-vfi OVERLAY
                     member pseudowire100
                     member pseudowire35 2.2.3.3 123 encapsulation mpls
                     member 10.10.10.10 123 encapsulation mpls
                     member 3.4.5.6 123 encapsulation mpls
                     member 5.3.2.1 123 template DVFR
                     member 5.5.5.5 444 template sdsd
                     member 5.5.5.5 123 encapsulation mpls
                     member 4.4.4.4 123 template RR
                     member 4.4.4.4 345 encapsulation mpls
                     member 4.4.4.4 14342 template TEST
                     member 4.4.4.4 423 encapsulation mpls
                     member pseudowire34 23.23.23.23 123 encapsulation mpls
                     member pseudowire23542 5.5.5.5 342 template BFD
                     member pseudowire23423
                     member vni 6060
                     device-tracking attach-policy example_policy
                     mdns-sd gateway
                      active-query timer 44
                      transport both
                      service-inst-suffix TEST2
                      service-mdns-query ptr
                      source-interface GigabitEthernet1/0/1
                      sdg-agent 6.6.6.6
                      service-policy TEST_POL
                    vlan configuration 11
                     member vfi VPLSVFI
                     member pseudowire36
                     member pseudowire101 4.5.6.7 333 template TETE
                     et-analytics enable
                     ipv6 destination-guard
                     ipv6 dhcp guard attach-policy TEST2
                     ipv6 nd ra-throttler
                     ipv6 nd raguard attach-policy TEST
                     ipv6 nd suppress
                    vlan configuration 12
                     member evpn-instance 354 vni 500100 protected
                     mdns-sd gateway
                     ipv6 destination-guard attach-policy TEST
                     ipv6 dhcp ldra attach-policy client-facing-untrusted
                     ipv6 dhcp guard
                     ipv6 nd ra-throttler attach-policy TEST2
                     ipv6 nd raguard
                     ipv6 nd suppress attach-policy TEST
                    """,
                ),
                state="parsed",
            ),
        )
        parsed = [
            {
                "vlan": "10",
                "member": {
                    "access_vfi": "OVERLAY",
                    "vni": "6060",
                    "pseudowire": [
                        {"pwnumber": "100"},
                        {"pwnumber": "35", "address": "2.2.3.3", "vc_id": "123"},
                        {"pwnumber": "34", "address": "23.23.23.23", "vc_id": "123"},
                        {"pwnumber": "23542", "address": "5.5.5.5", "vc_id": "342", "template": "BFD"},
                        {"pwnumber": "23423"},
                    ],
                    "ip_peer": [
                        {"address": "10.10.10.10", "vc_id": "123"},
                        {"address": "3.4.5.6", "vc_id": "123"},
                        {"address": "5.3.2.1", "vc_id": "123", "template": "DVFR"},
                        {"address": "5.5.5.5", "vc_id": "444", "template": "sdsd"},
                        {"address": "5.5.5.5", "vc_id": "123"},
                        {"address": "4.4.4.4", "vc_id": "123", "template": "RR"},
                        {"address": "4.4.4.4", "vc_id": "345"},
                        {"address": "4.4.4.4", "vc_id": "14342", "template": "TEST"},
                        {"address": "4.4.4.4", "vc_id": "423"},
                    ],
                },
                "mdns_sd_gateway": {
                    "enable": True,
                    "active_query_timer": "44",
                    "sdg_agent": "6.6.6.6",
                    "service_inst_suffix": "TEST2",
                    "service_mdns_query": "ptr",
                    "service_policy": "TEST_POL",
                    "source_interface": "GigabitEthernet1/0/1",
                    "transport": "both",
                },
                "device_tracking": {
                    "enable": True,
                    "attach_policy": "example_policy",
                },
            },
            {
                "vlan": "11",
                "member": {
                    "vfi": "VPLSVFI",
                    "pseudowire": [
                        {"pwnumber": "36"},
                        {"pwnumber": "101", "address": "4.5.6.7", "vc_id": "333", "template": "TETE"},
                    ],
                },
                "et_analytics_enable": True,
                "ipv6": {
                    "destination_guard": {
                        "enable": True,
                    },
                    "dhcp": {
                        "guard": {"enable": True, "attach_policy": "TEST2"},
                    },
                    "nd": {
                        "ra_throttler": {"enable": True},
                        "raguard": {"enable": True, "attach_policy": "TEST"},
                        "suppress": {"enable": True},
                    },
                },
            },
            {
                "vlan": "12",
                "member": {
                    "evpn": {
                        "instance": "354",
                        "vni": "500100",
                        "protected": True,
                    },
                },
                "mdns_sd_gateway": {
                    "enable": True,
                },
                "ipv6": {
                    "destination_guard": {
                        "enable": True,
                        "attach_policy": "TEST",
                    },
                    "dhcp": {
                        "guard": {"enable": True},
                        "ldra_attach_policy": "client-facing-untrusted",
                    },
                    "nd": {
                        "ra_throttler": {"enable": True, "attach_policy": "TEST2"},
                        "raguard": {"enable": True},
                        "suppress": {"enable": True, "attach_policy": "TEST"},
                    },
                },
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)
