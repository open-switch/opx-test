# opx_test
This smoketest contains the basic check on PAS, NAS, and CPS.
 
## Test cases

- Disable the logging on to syslog
- Dump the management interface 
- Dump the kernel routing table
- Check the `opx-cps` service is up
- Check the `redis-server` service is up
- Check the `opx-pas` service is up
- Check the `opx-nas` service is up
- Check the number of ports present with respect to the platform
- CPS get on the `base-pas` entity to check platform-related entities
- CPS get on the `base-pas` chassis to check burned MAC address
- Check the `opx-acl-init` service is up
- Check the `opx-qos-init` service is up
- Configure static route from kernel using "ip route" and check the route is programmed on the kernel
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
- Verify the system is up and running using `systemctl is-system-running`
- Verify the failed services using `systemctl --all --state=failed list-units`
- Dump the packages installed using `apt-list --installed`
- Verify the power supply, fan, and so on using `opx-show-env` which uses CPS Get
- Verify the media/optics present on the system using `opx-show-transceivers` which uses CPS Get

## How to run smoketest
**1**. Download ansible in any server (see [Ansible Installation](http://docs.ansible.com/ansible/intro_installation.html)).

**2**. Edit the `inventory.yaml` file with the details on the management IP, username, and password.

**3**. Run the playbook with the command below where `dut` is the variable specified in `inventory.yaml`.

    ansible-playbook opx_smoketest.yaml -i inventory.yaml --extra-vars "dut=baseHW"
 
See [opx-test](https://github.com/open-switch/opx-test/) for the `yaml` files.
 
(c) 2017 Dell
