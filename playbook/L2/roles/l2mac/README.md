# Role Name

This role is used to validate the MAC learning functionality of Layer2 with Flooding, Learning and Forwarding

# Requirements

The prerequisite for this role is to have the testbed ready with OPX installed. The testbed requirement here is to have 2 switches(DUT and TR) with OPX installed. 3 Links are connected between DUT and TR. 

1 link on Server1 is connected to DUT and 1 link on Server2 is connected to TR.  If you have ESXi VM, change the VLAN tag to 4095 to allow the tagged packets on the portgroups connected to DUT and TR. Hosts file needs to be named as DUT,TR,Server1 and Server2.

`Server1 <--(10g speed)---> DUT <----(3)----> TR <---(10g speed)--> Server2`

# Role Variables

The role variable file is defined in `vars/main.yml`. The sample file and the description of each is defined below.
```
vlanid:   100
unknownMAC:  "00:00:00:11:11:11"
dMAC:    "00:00:00:33:33:33"
staticMAC:    "00:00:00:22:22:22"
#server_link:    "ens192"
bond_interface:    "bond1"
```
* `vlanid` is the VLAN ID variable used for the test cases
* `unknownMAC` --- MAC address for flooding/forwarding
* `dMAC` is the destination MAC variable used for unicast traffic 
* `staticMAC` is the static MAC variable Used to configure static MAC on the port
* `bond_interface`is the portchannel interface variable used for the test cases

# Dependencies

Have the testbed ready with two switches OPX installed and 3 connections between the Switches. Have 2 VMs, one VM connected to DUT and another VM connected to TR with one link. If you are using ESXi VMs, enable VLAN 4095 to allowthe tagged packets on the portgroups connected to DUT and TR.

# Example Playbook

2host is the group created in /etc/ansible/hosts file which has DUT,TR,Server1 and Server2 mentioned.

```
- hosts: 2host
  gather_facts: false
  become: true
  pre_tasks:
     - setup:
  roles:
    - {role: L2/roles/l2mac, tags: ['l2mac']}
```
# TestCases
   * Verify Layer2 flooding/forwarding works on physical port
   * Verify Layer2 forwarding works with statically configured MAC on Physical Port
   * Verify Layer 2 forwarding works on LACP Portchannel
   * Verify Layer 2 forwarding works on Static Portchannel
   * Verify aging time set and learnt MAC addresses gets aged out 
# License

BSD

# Author Information

Madhusudhanan Santhanam - santhanam_madhusudha@dell.com
