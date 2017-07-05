# Quagga_L3_Test_Suite

This test suite consists of leaf/spine network with Open Source Routing package Quagga is running on all the switches. BGP is running between Leaf/Spine network. This test suite tests L3 Routing on Kernel/Hardware.

# Topology information
 
For this Test suite, all the links are 40G links.

Leaf1(L3-interface)-----Spine1(L3-interface)
Leaf1(L3-interface)-----Spine2(L3-interface)
Leaf2(L3-interface)-----Spine1(L3-interface)
Leaf2(L3-interface)-----Spine2(L3-interface)

# How the files are organized

roles--Contains the variables,files,tasks and handlers for the quagga L3 test suite 
ansible.cfg--Configuration file for ansible 
hosts--Defines the inventory of all the switches for ansible to manage
site.yml--yaml file to call the quagga l3 test suite playbook
host_vars--Contains the username/password for all the nodes encrypted using ansible vault

#roles/quagga_leaf_spine/
#tasks

main.yml -- Calls the quagga_leaf_spine.yml playbook, this playbook contains all the Test cases for quagga leaf spine network
traffic_ver_ECMP.yml---This file is for one of the test case to check traffic forwarding on ECMP paths between leaf/spine. This yml file is called 
                       in the quagga_leaf_spine.yml file itself.
traffic_ver_ECMP_shut.yml---This file is for one of the test case to check traffic forwarding after the ECMP is converted to non-ECMP path. This yml 
                            file is also called in quagga_leaf_spine.yml file itself.

#files

This folder contains all the files for generating the Quagga configuration file for each switch, route generation script, traffic generation script using mgen and necessary configuration files to set up Quagga.

#vars/main.yml

This file contains the necessary variables for all the switches to run all the test cases.

# Test Cases for Quagga L3 Test Suite

- Install Quagga application on OPX 
- Verify the quagga package is running
- Configure the IP address on L3 Physical interface
- Check IP address is programmed on all the L3 physical interface in Kernel/NAS
- Configure Quagga BGP between Leaf/Spine Switches
- Verify the BGP session is established on all the Leaf/Spine Switches
- Generate 500 BGP routes from Quagga BGP on Leaf2
- Verify all the 500 BGP routes are learnt in Kernel 
- Verify all the 500 BGP routes learnt with ECMP paths on NAS
- Install the open source traffic generator mgen on Leaf1
- Generate the traffic from Leaf1 to all the 500 BGP routes
- Verify the traffic is getting received on the ECMP paths on Leaf2
- Shut one of the ECMP link, check traffic still receives on Leaf2
- Bring up the link , check traffic gets received on ECMP paths again on Leaf2