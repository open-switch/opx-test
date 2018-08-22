# Role Name

This role is used to validate the mirroring functionality

# Requirements

The prerequisite for this role is to have the testbed ready with OPX installed. The testbed requirement here is to have 2 switches(DUT and TR) with OPX installed. 3 Links are connected between DUT and TR. 

1 link on Server1 is connected to DUT.  If you have ESXi VM, change the VLAN tag to 4095 to allow the tagged packets on the portgroups connected to DUT and TR. Hosts file needs to be named as DUT,TR,Server1 and Server2.

`Server1 <--(10g speed)---> DUT <----(3)----> TR`

# Role Variables

The role variable file is defined in `vars/main.yml`. The sample file and the description of each is defined below.
```
IPAddr1: "11.11.11.1"
IPAddr2: "11.11.11.2"
IPAddr3: "12.12.12.1"
IPAddr4: "12.12.12.2"
prefixlen:  "24"
lacpdMAC:  "01:80:C2:00:00:02"
lacpsMAC:  "00:44:00:00:00:00"
lacp_ethertype:   0x8809
dot1xdMAC:  "01:80:C2:00:00:03"
dot1xsMAC:  "00:44:00:22:33:44"
dot1x_ethertype:  0x888E
```
* `IPAddr1,IPAddr2,IPAddr3 and IPAddr4` defines the IP address configured on the interface
* `prefixlen` defines the prefix length/subnet mask
* `lacpdMAC` defines the LACP destination MAC variable used for traffic
* `lacpsMAC` defines the LACP source MAC variable used for traffic
* `lacp_ethertype` defines the LACP ethertype used for traffic
* `dot1xdMAC` defines the dot1x destination MAC address used for traffic
* `dot1xsMAC` defines the dot1x source MAC address used for traffic
* `dot1x_ethertype` defines the dot1x ether type used for traffic

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
    - {role: Forwarding/roles/span_mirroring, tags: ['span_mirroring']}
```
# TestCases

   * Verify_Span_Mirroring_Functionality 

# License

BSD

# Author Information

Madhusudhanan Santhanam - santhanam_madhusudha@dell.com
