# Smoke_test
This test contains the basic test cases on PAS,NAS and CPS.

## Requirements
- DHCP server should be enabled for the switch to get the management IP
- Outside connectivity should be there to install all the packages from bintray

## Files for ansible
- `ansible.cfg` — configuration file for Ansible
- `hosts` — hosts file to manage the hosts with hostname, userid, and password/key

## Folder structure and explanation
- `site.yml` — this YML file calls all YML files to install OPX Base and run the smoke test
- `roles/check_opx_onie` — contains the YML file to check whether the switch is in OPX prompt or ONIE prompt. If in OPX prompt, it will execute `onie_img_install` role, and install OPX Base.
- `roles/onie_img_install` —  role assumes the switch in OPX prompt, reboots the switch, and displays the ONIE prompt. After it comes to the ONIE prompt, it executes `check_opx_onie` role to install OPX Base.
- `roles/opx_smoke_test` — runs the smoke test to test PAS,NAS and CPS

## Variable file
`roles/opx_smoke_test/vars/opx_vars.yml` —  file contains the variables for the role `opx_smoke_test`

## Topology
The smoke test can be run on multiple nodes.

## Playbook functions
- Playbook (`check_opx_onie role`) will check whether the switch in ONIE prompt or OPX prompt
- If the switch in ONIE prompt (`check_opx_onie role`), it will uninstall the existing OS and install OPX
- If the switch in OPX prompt (`onie_img_install role`), it will reboot the switch to ONIE, uninstall the existing OS and install OPX
- Once the switch is up, `opx_smoke_test` will be triggered to run the smoke test

# Smoke test — test cases

- Disable the logging on to syslog
- Dump the management interface
- Dump the kernel routing table
- Check `opx-cps` service is up
- Check `redis-server` service is up
- Check `opx-pas` service is up
- Check `opx-nas` service is up
- Check the number of ports present with respect to the platform
- CPS get the `base-pas` entity to check platform-related entities
- CPS get the `base-pas` chassis to check burned MAC address
- Check `opx-acl-init` service is up
- Check `opx-qos-init` service is up
- Configure static route from kernel using *ip route* and check the route is programmed on the kernel
- CPS get on NAS to check whether the static route gets programmed on NAS
- Unconfiguring the static route in kernel
- Configure static MAC entry with VLAN using CPS Set
- Verify the MAC entry is present in NAS by using CPS Get
- Delete the static MAC entry with VLAN using CPS Set
- Verify the MAC entry is deleted in NAS by using CPS Get
- Add VLAN with untagged ports using CPS Set
- Verify VLAN with untagged ports on NAS using CPS Get
- Update the untagged ports on VLAN using CPS Set
- Verify the VLAN with updated ports on NAS using CPS Get
- Delete the VLAN using CPS set
- Verify the VLAN is removed from NAS using CPS Get
- Verify the system is up and running using systemctl is-system-running
- Verify the failed services using `systemctl --all --state=failed list-units`
- Dump the packages installed using `apt-list --installed`
- Verify the power supply, fan, and so on using `opx-show-env` which uses CPS Get
- Verify the media/optics present on the system using `opx-show-transceivers` which uses CPS Get

# How to run smoke test

1. Download ansible in any server/laptop (see Ansible Installation).
2. Edit the hosts file with the details on management IP, username, password/key (For onie_hostname, there needs to be separate host with username as root and password as empty, hostname which has default admin/admin username and password, check the sample hosts file)
3. Run the playbook with the command where *onie_hostname* is the hostname for OPX installation from ONIE, *hostname* is the OPX hostname, `IMG_LOCATION` is the location where the OPX image is located, and `IMG_NAME` is the name of the file which is copied to the tmp directory of ONIE.

    `ansible-playbook site.yml -i hosts --extra-vars "IMG_LOCATION=http://dell-networking.bintray.com/opx-images/opx-onie-installer_1.1_amd64.bin IMG_NAME=opx_image onie_hostname=ONIE_Leaf1 hostname=Leaf1" -vv`

See [opx-test](https://github.com/open-switch/opx-test) for all the files.

© 2017 Dell EMC
