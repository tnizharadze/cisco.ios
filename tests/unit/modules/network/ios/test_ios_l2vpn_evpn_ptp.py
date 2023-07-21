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

from ansible_collections.cisco.ios.plugins.modules import ios_l2vpn_evpn_ptp
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args
from deepdiff import DeepDiff

from .ios_module import TestIosModule


class TestIosL2VPNEVPNPTPModule(TestIosModule):
    module = ios_l2vpn_evpn_ptp

    def setUp(self):
        super(TestIosL2VPNEVPNPTPModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.l2vpn_evpn_ptp.l2vpn_evpn_ptp."
            "L2vpn_evpn_ptpFacts.get_l2vpn_evpn_ptp_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()
        self.maxDiff = None

    def tearDown(self):
        super(TestIosL2VPNEVPNPTPModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_l2vpn_evpn_ptp_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 123 point-to-point
             rd 222:222
             route-target export 33:44
             route-target import 33:44
             no auto-route-target
             vpws context TEST
              service target 44 source 77
              member Vlan10
              remote link failure notification
             !
             vpws context TEST2
              member Vlan11
              remote link failure notification
              shutdown
             !
            l2vpn evpn instance 124 point-to-point
             rd 333:333
             route-target export 43:45
             route-target import 43:45
             route-target export 45:55
             route-target import 45:55
             vpws context TEST3
              member Vlan12
              remote link failure notification
              shutdown
             !
             vpws context TEST4
              service target 55 source 55
              member Vlan14
              remote link failure notification
             !
            """,
        )
        gathered = [
            {
                "instance": "123",
                "rd": "222:222",
                "auto_route_target": False,
                "route_target_import": [
                    "33:44",
                ],
                "route_target_export": [
                    "33:44",
                ],
                "vpws_context": [
                    {
                        "context": "TEST",
                        "service": {
                            "target": "44",
                            "source": "77",
                        },
                        "member": "Vlan10",
                        "remote_link_failure_notification": True,
                    },
                    {
                        "context": "TEST2",
                        "member": "Vlan11",
                        "remote_link_failure_notification": True,
                        "shutdown": True,
                    },
                ],
            },
            {
                "instance": "124",
                "rd": "333:333",
                "auto_route_target": True,
                "route_target_import": [
                    "43:45",
                    "45:55",
                ],
                "route_target_export": [
                    "43:45",
                    "45:55",
                ],
                "vpws_context": [
                    {
                        "context": "TEST3",
                        "member": "Vlan12",
                        "remote_link_failure_notification": True,
                        "shutdown": True,
                    },
                    {
                        "context": "TEST4",
                        "service": {
                            "target": "55",
                            "source": "55",
                        },
                        "member": "Vlan14",
                        "remote_link_failure_notification": True,
                    },
                ],
            },
        ]
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        self.assertEqual({}, DeepDiff(result["gathered"], gathered, ignore_order=True))

    def test_ios_l2vpn_evpn_ptp_rendered(self):
        set_module_args(
            dict(
                config=[
                    {
                        "instance": "123",
                        "rd": "222:222",
                        "auto_route_target": False,
                        "route_target_import": [
                            "33:44",
                        ],
                        "route_target_export": [
                            "33:44",
                        ],
                        "vpws_context": [
                            {
                                "context": "TEST",
                                "service": {
                                    "target": "44",
                                    "source": "77",
                                },
                                "member": "Vlan10",
                                "remote_link_failure_notification": True,
                            },
                            {
                                "context": "TEST2",
                                "member": "Vlan11",
                                "remote_link_failure_notification": True,
                                "shutdown": True,
                            },
                        ],
                    },
                    {
                        "instance": "124",
                        "rd": "333:333",
                        "auto_route_target": True,
                        "route_target_import": [
                            "43:45",
                            "45:55",
                        ],
                        "route_target_export": [
                            "43:45",
                            "45:55",
                        ],
                        "vpws_context": [
                            {
                                "context": "TEST3",
                                "member": "Vlan12",
                                "remote_link_failure_notification": True,
                                "shutdown": True,
                            },
                            {
                                "context": "TEST4",
                                "service": {
                                    "target": "55",
                                    "source": "55",
                                },
                                "member": "Vlan14",
                                "remote_link_failure_notification": True,
                            },
                        ],
                    },
                ],
                state="rendered",
            ),
        )
        commands = [
            "l2vpn evpn instance 123 point-to-point",
            "rd 222:222",
            "no auto-route-target",
            "route-target export 33:44",
            "route-target import 33:44",
            "vpws context TEST",
            "service target 44 source 77",
            "member Vlan10",
            "remote link failure notification",
            "exit",
            "vpws context TEST2",
            "member Vlan11",
            "remote link failure notification",
            "shutdown",
            "exit",
            "exit",
            "l2vpn evpn instance 124 point-to-point",
            "rd 333:333",
            "route-target export 43:45",
            "route-target export 45:55",
            "route-target import 43:45",
            "route-target import 45:55",
            "vpws context TEST3",
            "member Vlan12",
            "remote link failure notification",
            "shutdown",
            "exit",
            "vpws context TEST4",
            "service target 55 source 55",
            "member Vlan14",
            "remote link failure notification",
            "exit",
            "exit",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_l2vpn_evpn_ptp_deleted_all(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 123 point-to-point
            l2vpn evpn instance 124 point-to-point
           """,
        )
        set_module_args(
            dict(
                config=[],
                state="deleted",
            ),
        )
        commands = [
            {
                "command": "no l2vpn evpn instance 123 point-to-point",
                "prompt": "yes/no",
                "answer": "yes",
            },
            {
                "command": "no l2vpn evpn instance 124 point-to-point",
                "prompt": "yes/no",
                "answer": "yes",
            },
        ]
        result = self.execute_module(changed=True)
        self.assertEqual({}, DeepDiff(result["commands"], commands, ignore_order=True))

    def test_ios_l2vpn_evpn_ptp_deleted_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 123 point-to-point
             rd 222:222
             route-target export 33:44
             route-target import 33:44
             no auto-route-target
             vpws context TEST
              service target 44 source 77
              member Vlan10
              remote link failure notification
             !
             vpws context TEST2
              member Vlan11
              remote link failure notification
              shutdown
             !
            l2vpn evpn instance 124 point-to-point
             rd 333:333
             route-target export 43:45
             route-target import 43:45
             route-target export 45:55
             route-target import 45:55
             vpws context TEST3
              member Vlan12
              remote link failure notification
              shutdown
             !
             vpws context TEST4
              service target 55 source 55
              member Vlan14
              remote link failure notification
             !
           """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "instance": "123",
                        "rd": "222:222",
                        "auto_route_target": False,
                        "route_target_import": [
                            "33:44",
                        ],
                        "route_target_export": [
                            "33:44",
                        ],
                        "vpws_context": [
                            {
                                "context": "TEST",
                                "service": {
                                    "target": "44",
                                    "source": "77",
                                },
                            },
                            {
                                "context": "TEST2",
                                "member": "Vlan11",
                                "remote_link_failure_notification": True,
                                "shutdown": True,
                            },
                        ],
                    },
                    {
                        "instance": "124",
                        "rd": "333:333",
                        "auto_route_target": True,
                        "route_target_import": [
                            "43:45",
                            "45:55",
                        ],
                        "route_target_export": [
                            "43:45",
                            "45:55",
                        ],
                        "vpws_context": [
                            {
                                "context": "TEST3",
                                "member": "Vlan12",
                                "remote_link_failure_notification": True,
                                "shutdown": True,
                            },
                            {
                                "context": "TEST4",
                                "service": {
                                    "target": "55",
                                    "source": "55",
                                },
                                "member": "Vlan14",
                                "remote_link_failure_notification": True,
                            },
                        ],
                    },
                ],
                state="deleted",
            ),
        )
        commands = [
            {
                "command": "no l2vpn evpn instance 124 point-to-point",
                "prompt": "yes/no",
                "answer": "yes",
            },
            "l2vpn evpn instance 123 point-to-point",
            "auto-route-target",
            "no rd 222:222",
            "no route-target import 33:44",
            "no route-target export 33:44",
            "vpws context TEST",
            "no service target 44 source 77",
            "exit",
            "no vpws context TEST2",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual({}, DeepDiff(result["commands"], commands, ignore_order=True))

    def test_ios_l2vpn_evpn_ptp_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 123 point-to-point
             rd 222:222
             route-target export 33:44
             route-target import 33:44
             no auto-route-target
             vpws context TEST
              service target 44 source 77
              member Vlan10
              remote link failure notification
             !
             vpws context TEST2
              member Vlan11
              remote link failure notification
              shutdown
             !
            l2vpn evpn instance 124 point-to-point
             rd 333:333
             route-target export 43:45
             route-target import 43:45
             route-target export 45:55
             route-target import 45:55
             vpws context TEST3
              member Vlan12
              remote link failure notification
              shutdown
             !
             vpws context TEST4
              service target 55 source 55
              member Vlan14
              remote link failure notification
             !
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "instance": "124",
                        "rd": "333:333",
                        "auto_route_target": False,
                        "route_target_import": [
                            "43:45",
                        ],
                        "route_target_export": [
                            "43:45",
                        ],
                        "vpws_context": [
                            {
                                "context": "TEST3",
                                "member": "Vlan11",
                                "remote_link_failure_notification": False,
                                "shutdown": False,
                            },
                            {
                                "context": "TEST4",
                                "service": {
                                    "target": "55",
                                    "source": "55",
                                },
                                "member": "Vlan14",
                                "remote_link_failure_notification": True,
                            },
                        ],
                    },
                ],
                state="replaced",
            ),
        )
        commands = [
            {
                "command": "no l2vpn evpn instance 123 point-to-point",
                "prompt": "yes/no",
                "answer": "yes",
            },
            "l2vpn evpn instance 124 point-to-point",
            "no auto-route-target",
            "no route-target export 45:55",
            "no route-target import 45:55",
            "vpws context TEST3",
            "no member Vlan12",
            "member Vlan11",
            "no remote link failure notification",
            "no shutdown",
            "exit",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual({}, DeepDiff(result["commands"], commands, ignore_order=True))

    def test_ios_l2vpn_evpn_ptp_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            l2vpn evpn instance 123 point-to-point
             rd 222:222
             route-target export 33:44
             route-target import 33:44
             no auto-route-target
             vpws context TEST
              service target 44 source 77
              member Vlan10
              remote link failure notification
             !
             vpws context TEST2
              member Vlan11
              remote link failure notification
              shutdown
             !
            l2vpn evpn instance 124 point-to-point
             rd 333:333
             route-target export 43:45
             route-target import 43:45
             route-target export 45:55
             route-target import 45:55
             vpws context TEST3
              member Vlan12
              remote link failure notification
              shutdown
             !
             vpws context TEST4
              service target 55 source 55
              member Vlan14
              remote link failure notification
             !
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "instance": "124",
                        "rd": "333:333",
                        "auto_route_target": True,
                        "route_target_import": [
                            "88:88",
                        ],
                        "route_target_export": [
                            "88:88",
                        ],
                        "vpws_context": [
                            {
                                "context": "TEST3",
                                "member": "Vlan12",
                                "remote_link_failure_notification": True,
                                "shutdown": True,
                            },
                            {
                                "context": "TEST4",
                                "service": {
                                    "target": "55",
                                    "source": "55",
                                },
                                "member": "Vlan11",
                                "remote_link_failure_notification": True,
                            },
                        ],
                    },
                ]
            )
        )
        commands = [
            "l2vpn evpn instance 124 point-to-point",
            "route-target export 88:88",
            "route-target import 88:88",
            "vpws context TEST4",
            "no member Vlan14",
            "member Vlan11",
            "exit",
            "exit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_l2vpn_evpn_ptp_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    l2vpn evpn instance 123 point-to-point
                     rd 222:222
                     route-target export 33:44
                     route-target import 33:44
                     no auto-route-target
                     vpws context TEST
                      service target 44 source 77
                      member Vlan10
                      remote link failure notification
                     !
                     vpws context TEST2
                      member Vlan11
                      remote link failure notification
                      shutdown
                     !
                    l2vpn evpn instance 124 point-to-point
                     rd 333:333
                     route-target export 43:45
                     route-target import 43:45
                     route-target export 45:55
                     route-target import 45:55
                     vpws context TEST3
                      member Vlan12
                      remote link failure notification
                      shutdown
                     !
                     vpws context TEST4
                      service target 55 source 55
                      member Vlan14
                      remote link failure notification
                     !
                    """,
                ),
                state="parsed",
            ),
        )
        parsed = [
            {
                "instance": "123",
                "rd": "222:222",
                "auto_route_target": False,
                "route_target_import": [
                    "33:44",
                ],
                "route_target_export": [
                    "33:44",
                ],
                "vpws_context": [
                    {
                        "context": "TEST",
                        "service": {
                            "target": "44",
                            "source": "77",
                        },
                        "member": "Vlan10",
                        "remote_link_failure_notification": True,
                    },
                    {
                        "context": "TEST2",
                        "member": "Vlan11",
                        "remote_link_failure_notification": True,
                        "shutdown": True,
                    },
                ],
            },
            {
                "instance": "124",
                "rd": "333:333",
                "auto_route_target": True,
                "route_target_import": [
                    "43:45",
                    "45:55",
                ],
                "route_target_export": [
                    "43:45",
                    "45:55",
                ],
                "vpws_context": [
                    {
                        "context": "TEST3",
                        "member": "Vlan12",
                        "remote_link_failure_notification": True,
                        "shutdown": True,
                    },
                    {
                        "context": "TEST4",
                        "service": {
                            "target": "55",
                            "source": "55",
                        },
                        "member": "Vlan14",
                        "remote_link_failure_notification": True,
                    },
                ],
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual({}, DeepDiff(result["parsed"], parsed, ignore_order=True))
