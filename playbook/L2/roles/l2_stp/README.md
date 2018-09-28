# Role Name

This role is used to validate the Layer 2 STP functionality

# Requirements

The prerequisite for this role is to have the testbed ready with OPX installed. The testbed requirement here is to have 2 switches(DUT and TR) with OPX installed. 3 Links are connected between DUT and TR. 

1 link on Server1 is connected to DUT and 1 link on Server2 is connected to TR.  If you have ESXi VM, change the VLAN tag to 4095 to allow the tagged packets on the portgroups connected to DUT and TR. Hosts file needs to be named as DUT,TR,Server1 and Server2.

`Server1 <--(1)---> DUT <----(3)----> TR <---(1)--> Server2`

# Role Variables

The role variables are defined in vars/main.yml, the file and the description for each variable is defined below.

```
vlanid:   100
unknownMAC:  "00:00:00:11:11:11"
dMAC:    "00:00:00:33:33:33"
staticMAC:    "00:00:00:22:22:22"
bond_interface:    "bond1"
```

* `vlanid` defines the VLAN ID used for the test cases
* `unknownMAC` defines the MAC address for flooding/forwarding
* `dMAC` defines the destination MAC used for unicast traffic 
* `staticMAC` defines the static MAC configuration on the port
* `bond_interface` defines the portchannel interface used for the test cases

# Dependencies

Have the testbed ready with two switches OPX installed and 3 connections between the Switches. Have 2 VMs, one VM connected to DUT and another VM connected to TR with one link. If you are using ESXi VMs, enable VLAN 4095 to allow the tagged packets on the portgroups connected to DUT and TR.

# Example Playbook

2host is the group created in /etc/ansible/hosts file which has DUT,TR,Server1 and Server2 mentioned.

```
- hosts: 2host
  gather_facts: false
  become: true
  pre_tasks:
     - setup:
  roles:
    - {role: L2/roles/l2_stp, tags: ['l2_stp']}
```

# TestCases

   * Verify_STP_convergence_with_traffic

# License

BSD

# Author Information

Madhusudhanan Santhanam - santhanam_madhusudha@dell.com
