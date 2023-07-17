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

from ansible_collections.cisco.ios.plugins.modules import ios_l2vpn_evpn_vb
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule

class TestIosL2VPNEVPNVBModule(TestIosModule):
    module = ios_l2vpn_evpn_vb

    def setUp(self):
        super(TestIosL2VPNEVPNVBModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.l2vpn_evpn_vb.l2vpn_evpn_vb."
            "L2vpn_evpn_vbFacts.get_l2vpn_evpn_vb_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()
        self.maxDiff = None

    def tearDown(self):
        super(TestIosL2VPNEVPNVBModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_l2vpn_evpn_vb_gathered(self):
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
        gathered = [
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
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        for each in gathered:
            each["route_target_import"] = set(each["route_target_import"])
            each["route_target_export"] = set(each["route_target_export"])
        for each in result["gathered"]:
            each["route_target_import"] = set(each["route_target_import"])
            each["route_target_export"] = set(each["route_target_export"])
        self.assertEqual(result["gathered"], gathered)


    def test_ios_l2vpn_evpn_vb_rendered(self):
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
            "auto-route-target",
            "default-gateway advertise disable",
            "multicast advertise enable",
            "exit",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_l2vpn_evpn_vb_deleted_idempotent(self):
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

    def test_ios_l2vpn_evpn_vb_replaced_idempotent(self):
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


    def test_ios_l2vpn_evpn_vb_merged_idempotent(self):
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


    def test_ios_l2vpn_evpn_vb_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
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
                    "444:555",
                    "333:444",
                ],
                "route_target_export": [
                    "444:555",
                    "333:444",
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
        self.assertEqual(result["parsed"], parsed)