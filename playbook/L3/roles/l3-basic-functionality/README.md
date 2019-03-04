Role Name
=========

This role is used to validate l3 functionality on NAS: Layer3 Ip Address configuration and hardware programming Static route and layer 3 forwarding. 

Requirements
------------

The prerequisite for this role is to have the testbed ready with OPX installed. The testbed requirement here is to have 2 switches(DUT and TR) with OPX installed. 3 Links are connected between DUT and TR. 

1 link on Server1 is connected to DUT and 1 link on Server2 is connected to TR.  If you have ESXi VM, change the VLAN tag to 4095 to allow the tagged packets on the portgroups connected to DUT and TR. Hosts file needs to be named as DUT,TR,Server1 and Server2.

Server1 <--(1)---> DUT <----(3)----> TR <---(1)--> Server2

Role Variables
--------------

The group variables which is common for all the roles are defined in /etc/ansible/playbook/group_vars file. The description of each is defined below.

The variables for  l3-basic-functionality are defined in vars/main.yml file. The description of each is defined below.

```
IPAddr1: "10.1.1.1"
prefixlen: "24"
IPAddr2: "10.1.1.2"
route0: "10.1.1.0/24"
bond_interface: "bond100"
bridge: "br100"
vlanid: "100"
route1: "200.1.1.0/24"
route2: "201.1.1.0/24"
IPAddr3: "200.1.1.1"
IPAddr4: "200.1.1.2"
IPAddr5: "201.1.1.1"
IPAddr6: "201.1.1.2"
speed: "40g"
splitspeed: "10g"
```

* `IPAddr1,IPAddr2,IPAddr3, IPAddr4, IPAddr5 and IPAddr6` defines the IP address configured on the interface
* `prefixlen` defines the prefix length/subnet mask
* `bridge` defines the VLAN bridge
* `route0, route1 and route2` defines the static routes used for the test cases
* `vlanid` is the VLAN ID variable used for the test cases
* `bond_interface`is the portchannel interface variable used for the test cases
* `splitspeed` is to define the speed of the split/fanout port
* `speed` is to define the speed of the fanin port

Dependencies
------------

Have the testbed ready with two switches OPX installed and 3 connections between the Switches. Have 2 VMs, one VM connected to DUT and another VM connected to TR with one link. If you are using ESXi VMs, enable VLAN 4095 to allow the tagged packets on the portgroups connected to DUT and TR.

Example Playbook
----------------

- hosts: 2host
  gather_facts: false
  tags: l3-basic-functionality
  become: true
  pre_tasks:
     - setup:
  vars_files:
    - '/etc/ansible/playbook/L2/roles/l3-basic-functionality/vars/main.yml'
  roles:
    - {role: L3/roles/l3-basic-functionality, tags: ['l3-basic-functionality']}

2host is the group created in /etc/ansible/hosts file which has DUT,TR,Server1 and Server2 mentioned.

TestCases
---------
1. Verify arp got resolved and ping works on lag interface 
2. Verify user can add modify and delete ipv4 address to a fanout interface
3. Verify ping works between fannout interfaces
4. Verify ping works between physical interfaces
5. Verify user can add modify and delete ipv4 address to a lag interface
6. Verify user can add modify and delete ipv4 address to a vlan_interface
7. Verify_arp_get_resolved_and_ping_works_on_vlan_interface
8. Verify_user_can_add_modify_and_delete_Ipv4_address_to_a_physical_interface
9. Verify static route configuration works 

License
-------

BSD

Author Information
------------------

Tejaswi Goel - tejaswi_goel@dell.com
