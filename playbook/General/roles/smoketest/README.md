# Role Name

This role is used for smoketest.

# Requirements

The prerequisite for this role is to have DUT with OPX installed and have optic in one of the port.

# Role Variables

The role variable file is defined in vars/main.yml. The file and the description of each variable is defined below.

```
test_route1:    100.0.0.1
test_route2:    20.0.0.0
test_mac   :    00:11:22:33:44:55
test_vlan  :    100
test_prefix:    24
test_cps_prefix: 32
test_route2hex: 14000000
test_via:       100.0.0.2
```
* `test_int,test_int1` defines the interfaces used for smoketest
* `test_route1,test_route2` defines the IP addresses used to verify/configure 
* `test_mac` defines the variable used for L2 functionality test in smoketest
* `test_vlan` defines the VLAN used for L2 functionality in smoketest
* `test_prefix` defines the variable used for prefix length used for L3 test in smoketest
* `test_cps_prefix` defines the variable used for host prefix check for L3 test in smoketest
* `test_route2hex`defines the variable used for converted IP address to hexadecimal value to check on CPS get
* `test_via` defines the Static route variable
* `test_mgmtint` defines the Management interface

# Dependencies

DUT with OPX installed and have optic in one of the port.

# Example Playbook

1host is the group created in `/etc/ansible/hosts` file which has DUT mentioned.

```
- hosts: 1host
  gather_facts: false
  pre_tasks:
    - setup:
  become: true
  roles:
    - {role: General/roles/smoketest, tags: ['smoketest']}
```
# TestCases

* Disable the logging on to syslog
* Dump the management interface
* Dump the kernel routing table
* Check the opx-cps service is up
* Check the redis-server service is up
* Check the opx-pas service is up
* Check the opx-nas service is up
* Check the number of ports present with respect to the platform
* CPS get on the base-pas entity to check platform-related entities
* CPS get on the base-pas chassis to check burned MAC address
* Check the opx-acl-init service is up
* Check the opx-qos-init service is up
* Configure static route from kernel using "ip route" and check the route is programmed on the kernel
* CPS get on NAS to check whether the static route gets programmed on NAS
* Unconfiguring the static route in kernel
* Configure static MAC entry with VLAN using CPS Set
* Verify the MAC entry is present in NAS by using CPS Get
* Delete the static MAC entry with VLAN using CPS Set
* Verify the MAC entry is deleted in NAS by using CPS Get
* Add VLAN with untagged ports using CPS Set
* Verify VLAN with untagged ports on NAS using CPS Get
* Update the untagged ports on VLAN using CPS Set
* Verify the VLAN with updated ports on NAS using CPS Get
* Delete the VLAN using CPS set
* Verify the VLAN is removed from NAS using CPS Get
* Verify the system is up and running using systemctl is-system-running
* Verify the failed services using systemctl --all --state=failed list-units
* Dump the packages installed using apt-list --installed
* Verify the power supply, fan, and so on using opx-show-env which uses CPS Get
* Verify the media/optics present on the system using opx-show-transceivers which uses CPS Get

# License

BSD

# Author Information

Madhusudhanan Santhanam - santhanam_madhusudha@dell.com
