# Zero_Touch

This test contains the zero touch provisioning where the switch will install the OPX OS from ONIE, install all the packages and runs the smoke test.

# Requirements

DHCP server should be enabled for the switch to get the management IP
Outside connectivity should be there to install all the packages from bintray
Ansible should be installed on any server/laptop

# Files for ansible

ansible.cfg- Configuration file for ansible
hosts- Hosts file to manage the hosts with hostname, userid and password/key

# Folder structure and Explanation

site.yml - This yml file calls all the yml files to install OPX NOS and run smoke test
roles/check_opx_onie - This role contains the yml file to check whether the switch in OPX prompt or ONIE prompt, if in OPX prompt it will execute 
                       onie_img_install role. It will install the OPX NOS.
roles/onie_img_install - This role assumes the switch in OPX prompt, reboot the switch and bring to ONIE prompt. After it comes to ONIE prompt, it will execute check_opx_onie role to install OPX NOS
roles/pkg_install - This role will install all the packages NAS, PAS and CPS.
roles/pkg_upgrade - This role will upgrade all the packages
roles/opx_smoke_test- This will run the smoke test to test PAS,NAS and CPS

# Variable files

roles/check_opx_onie/vars/main.yml - This file contains the variables for the role check_opx_onie
roles/opx_smoke_test/vars/opx_vars.yml - This file contains the variables for the role opx_smoke_test

# Topology

This zero touch runs on any node mentioned in the hosts file

# Playbook functions
- Playbook(check_opx_onie role) will check whether the switch in ONIE prompt or OPX prompt. 
- If the switch in ONIE prompt(check_opx_onie role), it will uninstall the existing OS and install OPX.
- If the switch in OPX prompt(onie_img_install role), it will reboot the switch to ONIE, uninstall the existing OS and install OPX
- After the OPX is installed, it will install the packages using "apt-get install opx-dell-s6000"(role is pkg_install) and reboot the switch
- if the switch only needs upgrade of packages instead of reboot, pkg_upgrade role needs to be triggered. After the upgrade is done, the switch will reboot and comes up.
- Once the switch is up, opx_smoke_test will be triggered to run the smoke test


# Smoke Test Test Cases

- Disable the logging on to syslog
- Dump the management interface
- Dump the kernel routing table
- Check the opx-cps service is up
- Check the redis-server service is up
- Check the opx-pas service is up
- Check the opx-nas service is up
- Check the number of ports present with respect to the platform
- CPS get on the base-pas entity to check platform-related entities
- CPS get on the base-pas chassis to check burned MAC address
- Check the opx-acl-init service is up
- Check the opx-qos-init service is up
- Configure static route from kernel using "ip route" and check the route is programmed on the kernel
- CPS get on NAS to check whether the static route gets programmed on NAS
- Unconfiguring the static route in kernel
- Add VLAN with untagged ports using CPS Set
- Verify VLAN with untagged ports on NAS using CPS Get
- Update the untagged ports on VLAN using CPS Set
- Verify the VLAN with updated ports on NAS using CPS Get
- Delete the VLAN using CPS set
- Verify the VLAN is removed from NAS using CPS Get
- Verify the system is up and running using systemctl is-system-running
- Verify the failed services using systemctl --all --state=failed list-units
- Dump the packages installed using apt-list --installed
- Verify the power supply, fan, and so on using opx-show-env which uses CPS Get
- Verify the media/optics present on the system using opx-show-transceivers which uses CPS Get

# How to run zero touch

1. Download ansible in any server/laptop(see Ansible Installation).
2. Edit the hosts file with the details on management IP, username, password/key (For ONIE, there need-s to be seperate host with username as root, check the sample hosts file)
3. Under the host_vars file ,username and password is mentioned for each host and is encrypted using ansible-vault
4. Run the playbook with the command where 'hostname' is the hostname for OPX installation from ONIE, IMG_LOCATION is the location where the OPX image is located and IMG_NAME is the name of the file which is copied to the tmp directory of ONIE
    
    - Example adhoc ansible command for running the full blown zero_touch with smoke_test

      ansible-playbook -i $inventory $playbook --tags "zero_touch" --extra-vars "IMG_LOCATION=$IMG_LOCATION IMG_NAME=$IMG_NAME hostname=$HOSTNAME" -vv --vault-password-file=vault_password.txt

      inventory - hosts file containing all the hosts to manage (check the sample hosts file)
      playbook - site.yml file will call the roles
      IMG_LOCATION- Location of the OPX image to copy it to ONIE
      IMG_NAME - Name of the file to copy to ONIE(can be anything)
      hostname - This hostname should be ONIE_$hostname which is used to login to switch using root to check the switch in ONIE prompt
      vault-password- Encrypted the host_vars file using ansible-vault (used if needed)
    
    - Example adhoc ansible command to run only the upgrade/smoke_test
      
      ansible-playbook -i $inventory $playbook --tags "smoke_test" --extra-vars "IMG_LOCATION=$IMG_LOCATION IMG_NAME=$IMG_NAME hostname=$HOSTNAME" -vv --vault-password-file=vault_password.txt
     
Check zero_touch folder for all the files.