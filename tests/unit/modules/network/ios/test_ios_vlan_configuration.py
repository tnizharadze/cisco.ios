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
            vlan configuration 11
             member vfi VPLSVFI
             member pseudowire36
             member pseudowire101 4.5.6.7 333 template TETE
            """,
        )
        gathered = [
            {
                "vlan": "10",
                "member": {
                    "access_vfi": "OVERLAY",
                    "pseudowire": [
                        {"pwnumber": "100"},
                        {"pwnumber": "35",
                         "address": "2.2.3.3",
                         "vc_id": "123",
                         "encapsulation_mpls": True},
                        {"pwnumber": "34",
                         "address": "23.23.23.23",
                         "vc_id": "123",
                         "encapsulation_mpls": True},
                        {"address": '5.5.5.5',
                         "pwnumber": '23542',
                         "template": 'BFD',
                         "vc_id": '342'},
                        {"pwnumber": '23423'}
                    ],
                },
            },
            {
                "vlan": "11",
                "member": {
                    "vfi": "VPLSVFI",
                    "pseudowire": [
                        {"pwnumber": "36"},
                        {"pwnumber": "101",
                         "address": "4.5.6.7",
                         "vc_id": "333",
                         "template": "TETE"},
                    ],
                },
            },
        ]
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def _test_ios_vlan_configuration_rendered(self):
        set_module_args(
            dict(
                config=[
                    {
                        "instance": "124",
                        "auto_route_target": False,
                        "default_gateway_advertise": "enable",
                        "encapsulation": "vxlan",
                        "ip_local_learning": "disable",
                        "multicast_advertise": "disable",
                        "rd": "65374:103",
                        "re_originate_route_type5": True,
                        "replication_type": "ingress",
                        "route_target_import": [
                            "333:444",
                            "444:555",
                        ],
                        "route_target_export": [
                            "333:444",
                            "444:555",
                        ],
                    },
                    {
                        "instance": "126",
                        "auto_route_target": True,
                        "default_gateway_advertise": "disable",
                        "encapsulation": "vxlan",
                        "ip_local_learning": "enable",
                        "multicast_advertise": "enable",
                        "rd": "65500:200",
                        "replication_type": "static",
                        "route_target_import": [
                            "444:555",
                            "666:111",
                        ],
                        "route_target_export": [
                            "444:555",
                            "666:111",
                        ],
                    },
                ],
                state="rendered",
            ),
        )
        commands = [
            "l2vpn evpn instance 124 vlan-based",
            "encapsulation vxlan",
            "no auto-route-target",
            "rd 65374:103",
            "route-target export 444:555",
            "route-target import 444:555",
            "route-target export 333:444",
            "route-target import 333:444",
            "ip local-learning disable",
            "replication-type ingress",
            "default-gateway advertise enable",
            "multicast advertise disable",
            "re-originate route-type5",
            "exit",
            "l2vpn evpn instance 126 vlan-based",
            "encapsulation vxlan",
            "rd 65500:200",
            "route-target export 444:555",
            "route-target import 444:555",
            "route-target export 666:111",
            "route-target import 666:111",
            "replication-type static",
            "ip local-learning enable",
            "default-gateway advertise disable",
            "multicast advertise enable",
            "exit",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def _test_ios_vlan_configuration_deleted_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 124 vlan-based
             encapsulation vxlan
             rd 65374:103
             route-target export 444:555
             route-target import 444:555
             route-target export 333:444
             route-target import 333:444
             ip local-learning disable
             no auto-route-target
             replication-type ingress
             default-gateway advertise enable
             multicast advertise disable
             re-originate route-type5
            l2vpn evpn instance 126 vlan-based
             encapsulation vxlan
             rd 65500:200
             route-target export 444:555
             route-target import 444:555
             route-target export 666:111
             route-target import 666:111
             replication-type static
             ip local-learning enable
             default-gateway advertise disable
           """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "instance": "124",
                        "auto_route_target": False,
                        "default_gateway_advertise": "enable",
                        "encapsulation": "vxlan",
                        "ip_local_learning": "disable",
                        "multicast_advertise": "disable",
                        "rd": "65374:103",
                        "re_originate_route_type5": True,
                        "replication_type": "ingress",
                        "route_target_import": [
                            "333:444",
                            "444:555",
                        ],
                        "route_target_export": [
                            "333:444",
                            "444:555",
                        ],
                    },
                    {
                        "instance": "126",
                        "auto_route_target": True,
                        "encapsulation": "vxlan",
                        "ip_local_learning": "enable",
                        "multicast_advertise": "disable",
                        "rd": "65500:200",
                        "replication_type": "static",
                        "route_target_import": [
                            "444:555",
                            "666:111",
                        ],
                        "route_target_export": [
                            "444:555",
                            "666:111",
                        ],
                    },
                ],
                state="deleted",
            ),
        )
        commands = [
            "no l2vpn evpn instance 124 vlan-based",
            "l2vpn evpn instance 126 vlan-based",
            "no auto-route-target",
            "no encapsulation vxlan",
            "no ip local-learning enable",
            "no rd 65500:200",
            "no replication-type static",
            "no route-target import 444:555",
            "no route-target import 666:111",
            "no route-target export 666:111",
            "no route-target export 444:555",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def _test_ios_vlan_configuration_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 124 vlan-based
             encapsulation vxlan
             rd 65374:103
             route-target export 444:555
             route-target import 444:555
             route-target export 333:444
             route-target import 333:444
             ip local-learning disable
             no auto-route-target
             replication-type ingress
             default-gateway advertise enable
             multicast advertise disable
             re-originate route-type5
            l2vpn evpn instance 126 vlan-based
             encapsulation vxlan
             rd 65500:200
             route-target export 444:555
             route-target import 444:555
             route-target export 666:111
             route-target import 666:111
             replication-type static
             ip local-learning enable
             default-gateway advertise disable
             multicast advertise enable
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "instance": "126",
                        "auto_route_target": True,
                        "default_gateway_advertise": "enable",
                        "encapsulation": "vxlan",
                        "ip_local_learning": "enable",
                        "multicast_advertise": "enable",
                        "rd": "65500:200",
                        "replication_type": "ingress",
                        "route_target_import": [
                            "444:555",
                        ],
                        "route_target_export": [
                            "444:555",
                        ],
                    },
                ],
                state="replaced",
            ),
        )
        commands = [
            "no l2vpn evpn instance 124 vlan-based",
            "l2vpn evpn instance 126 vlan-based",
            "no route-target import 666:111",
            "no route-target export 666:111",
            "default-gateway advertise enable",
            "replication-type ingress",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def _test_ios_vlan_configuration_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "instance": "124",
                        "auto_route_target": False,
                        "encapsulation": "vxlan",
                    },
                ]
            )
        )
        commands = [
            "l2vpn evpn instance 124 vlan-based",
            "encapsulation vxlan",
            "no auto-route-target",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def _test_ios_vlan_configuration_merged_idempotent2(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 124 vlan-based
             encapsulation vxlan
             rd 65374:103
             route-target export 444:555
             route-target import 444:555
             route-target export 333:444
             route-target import 333:444
             ip local-learning disable
             no auto-route-target
             replication-type ingress
             default-gateway advertise enable
             multicast advertise disable
             re-originate route-type5
            l2vpn evpn instance 126 vlan-based
             encapsulation vxlan
             rd 65500:200
             route-target export 444:555
             route-target import 444:555
             route-target export 666:111
             route-target import 666:111
             replication-type static
             ip local-learning enable
             default-gateway advertise disable
             multicast advertise enable
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "instance": "124",
                        "auto_route_target": True,
                        "default_gateway_advertise": "enable",
                        "encapsulation": "vxlan",
                        "ip_local_learning": "disable",
                        "multicast_advertise": "disable",
                        "rd": "65374:103",
                        "re_originate_route_type5": True,
                        "replication_type": "ingress",
                        "route_target_import": [
                            "333:444",
                            "444:555",
                            "222:777",
                        ],
                        "route_target_export": [
                            "333:444",
                            "444:555",
                            "222:777",
                        ],
                    },
                    {
                        "instance": "126",
                        "auto_route_target": False,
                        "default_gateway_advertise": "disable",
                        "encapsulation": "vxlan",
                        "ip_local_learning": "disable",
                        "multicast_advertise": "enable",
                        "rd": "65500:200",
                        "replication_type": "ingress",
                        "route_target_import": [
                            "444:555",
                            "666:111",
                        ],
                        "route_target_export": [
                            "444:555",
                            "666:111",
                        ],
                    },
                ],
                state="merged",
            ),
        )
        commands = [
            "l2vpn evpn instance 124 vlan-based",
            "auto-route-target",
            "route-target export 222:777",
            "route-target import 222:777",
            "exit",
            "l2vpn evpn instance 126 vlan-based",
            "no auto-route-target",
            "ip local-learning disable",
            "replication-type ingress",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def _test_ios_vlan_configuration_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    l2vpn evpn instance 124 vlan-based
                     encapsulation vxlan
                     rd 65374:103
                     route-target export 333:444
                     route-target import 333:444
                     route-target export 444:555
                     route-target import 444:555
                     ip local-learning disable
                     no auto-route-target
                     replication-type ingress
                     default-gateway advertise enable
                     multicast advertise disable
                     re-originate route-type5
                    l2vpn evpn instance 126 vlan-based
                     encapsulation vxlan
                     rd 65500:200
                     route-target export 666:111
                     route-target import 666:111
                     route-target export 444:555
                     route-target import 444:555
                     replication-type static
                     ip local-learning enable
                     default-gateway advertise disable
                     multicast advertise enable
                    """,
                ),
                state="parsed",
            ),
        )
        parsed = [
            {
                "instance": "124",
                "auto_route_target": False,
                "default_gateway_advertise": "enable",
                "encapsulation": "vxlan",
                "ip_local_learning": "disable",
                "multicast_advertise": "disable",
                "rd": "65374:103",
                "re_originate_route_type5": True,
                "replication_type": "ingress",
                "route_target_import": [
                    "333:444",
                    "444:555",
                ],
                "route_target_export": [
                    "333:444",
                    "444:555",
                ],
            },
            {
                "instance": "126",
                "auto_route_target": True,
                "default_gateway_advertise": "disable",
                "encapsulation": "vxlan",
                "ip_local_learning": "enable",
                "multicast_advertise": "enable",
                "rd": "65500:200",
                "replication_type": "static",
                "route_target_import": [
                    "444:555",
                    "666:111",
                ],
                "route_target_export": [
                    "444:555",
                    "666:111",
                ],
            },
        ]
        result = self.execute_module(changed=False)
        for each in result["parsed"]:
            each["route_target_import"] = sorted(each["route_target_import"])
            each["route_target_export"] = sorted(each["route_target_export"])
        self.assertEqual(result["parsed"], parsed)
