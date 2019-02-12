# Role Name

This role is used to validate that LAG configurations are working fine

# Requirements

The prerequisite for this role is to have the testbed ready with OPX installed. The testbed requirement here is to have 1 switch(DUT) with OPX installed. 


# Role Variables

The role variable file is defined in `vars/main.yml`. The sample file and the description of each is defined below.
```
lagid:   100
unknownMAC:  "00:00:00:11:11:11"
dMAC:    "00:00:00:33:33:33"
staticMAC:    "00:00:00:22:22:22"
bond_interface:    "bond1"

```
* `lagid` is the LAG ID variable used for the test cases
* `unknownMAC` --- MAC address for flooding/forwarding
* `dMAC` is the destination MAC variable used for unicast traffic 
* `staticMAC` is the static MAC variable Used to configure static MAC on the port
* `bond_interface`is the portchannel interface variable used for the test cases

# Dependencies

Have the testbed ready with a switch with OPX installed.

# Example Playbook

1host is the group created in /etc/ansible/hosts file which just has a DUT.

```
- hosts: 1host
  gather_facts: false
  become: true
  pre_tasks:
     - setup:
  roles:
    - {role: L2/roles/lagConfig, tags: ['lagConfig']}
```
# TestCases
   * Verify LAG Creation is successful
   * Verify if the LAG show output matches the expected syntax
   * Verify if a blocked port could be added to the LAG
   * Verify if an unblocked port could be added to the LAG
   * Verify if a blocked port could be removed from the LAG
   * Verify if an unblocked port could be removed from the LAG
   * Verify if the blocked port list of the LAG could be force set to a given port-list
   * Verify if the unblocked port list of the LAG could be force set to a given port-list
   * Verify if a new LAG with the same LAG ID that of an existing LAG could be created
   * Verify LAG Deletion is successful
# License

BSD

# Author Information

Rakesh Datta - rakesh.datta@dell.com
