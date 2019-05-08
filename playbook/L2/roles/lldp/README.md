Role Name
=========

This role is used to validate LLDP Service before and after the event and check the LLDP functionality by checking the keywords like chassisid, sysname,sysdescr,mgmtip,portid,portdescr

Requirements
------------

The prerequisite for this role is to have the testbed ready with OPX installed. The testbed requirement here is to have 2 switches(DUT and TR) with OPX installed. 1 Link are connect between DUT and TR. 

1 link on Server1 is connected to DUT and 1 link on Server2 is connected to TR.  
DUT <----(1)----> TR 

Dependencies
------------

Have the testbed ready with two switches OPX installed and 3 connections between the Switches. Have 2 VMs, one VM connected to DUT and another VM connected to TR with one link. 

Example Playbook
----------------

- hosts: 1host
  gather_facts: false
  tags: lldp
  become: true
  roles:
    - {role: L2/roles/lldp, tags: ['lldp']}

2host is the group created in /etc/ansible/hosts file which has DUT and TR are mentioned.

TestCases
---------

1. Verify LLDP Service before and after the event
2. Check the LLDP functionality by checking the keywords chassisid
3. Check the LLDP functionality by checking the keywords sysname
4. Check the LLDP functionality by checking the keywords sysdescr
5. Check the LLDP functionality by checking the keywords mgmtip

License
-------

BSD

Author Information
------------------

Tejaswi Goel - tejaswi_goel@dell.com
