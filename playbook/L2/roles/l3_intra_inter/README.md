# Role Name

This role is used to validate the Layer 3 Intra and InterVLAN functionality

# Requirements

The prerequisite for this role is to have the testbed ready with OPX installed. The testbed requirement here is to have 2 switches(DUT and TR) with OPX installed. 3 Links are connected between DUT and TR. 

1 link on Server1 is connected to DUT and 1 link on Server2 is connected to TR.  If you have ESXi VM, change the VLAN tag to 4095 to allow the tagged packets on the portgroups connected to DUT and TR. Hosts file needs to be named as DUT,TR,Server1 and Server2.

`Server1 <--(1)---> DUT <----(3)----> TR <---(1)--> Server2`

# Role Variables

The role variables are defined in vars/main.yml, the file content and description of each variable is defined below.

```
vlanid:   100
interVLAN: 200
unknownMAC:  "00:00:00:11:11:11"
dMAC:    "00:00:00:33:33:33"
staticMAC:    "00:00:00:22:22:22"
IPAddr1:    "100.1.1.1"
IPAddr2:    "100.1.1.3"
IPAddr3:    "100.1.1.2"
interVLANIP1:    "101.1.1.1"
interVLANIP2:    "101.1.1.2"
prefixlen:    "24"
hostprefix:    "32"
bond_interface:    "bond1"
```

* `vlanid` defines the VLAN ID used for the test cases
* `interVLAN` defines the VLAN ID used for intervlan routing
* `unknownMAC` defines the MAC address for flooding/forwarding
* `dMAC` defines the destination MAC used for unicast traffic 
* `staticMAC` defines the static MAC addresss on the port
* `IPAddr1, IPAddr2 and IPAddr3` defines the IP address used for IntraVLAN functionality
* `interVLANIP1 and interVLANIP2` defines the IP addresses used for InterVLAN functionality
* `prefixlen` defines the subnet mask for InterVLAN and IntraVLAN
* `hostprefix` defines the subnet mask used for the static route between intra and interVLAN
* `bond_interface` defines the portchannel interface used for the test cases

# Dependencies

Have the testbed ready with two switches OPX installed and 3 connections between the Switches. Have 2 VMs, one VM connected to DUT and another VM connected to TR with one link. If you are using ESXi VMs, enable VLAN 4095 to allow the tagged packets on the portgroups connected to DUT and TR.

# Example Playbook

2host is the group created in /etc/ansible/opx/hosts file which has DUT,TR,Server1 and Server2 mentioned.

```
- hosts: 2host
  gather_facts: false
  become: true
  pre_tasks:
     - setup:
  roles:
    - {role: L2/roles/l3_intra_inter, tags: ['l3_intra_inter']}
```

# TestCases

   * Verify_Intra_VLAN_Routing_With_Tagged_Access_Ports
   * Verify_Inter_VLAN_Routing_With_Tagged_Access_Ports

# License

BSD

# Author Information

Madhusudhanan Santhanam - santhanam_madhusudha@dell.com
