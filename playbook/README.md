# site.yml

Playbook roles are defined in site.yml
Below is an example of a playbook defined.
```
- hosts: 1host
  gather_facts: false
  pre_tasks:
    - setup:
  become: true
  roles:
    - {role: General/roles/smoketest, tags: ['smoketest']}
```
* `hosts` is to defined on which group smoketest has to run. Defined as 1host where the smoketest needed only one host
* `gather_facts` is set to false on not to gather the facts from switch
* `become` is to run the commands in sudo mode
* `roles` is where the playbook/script is defiined under the folder `General/roles/smoketest/tasks/smoketest.yaml`
* `tags` is important here to specify a particular playbook to run
* `variables` for the `smoketest` are defined under the same folder `General/roles/smoketest/vars/main.yml`and similary for `l2mac` defined in `L2/roles/l2mac/vars/main.yml`

# host_vars

All the interface connections for each host is defined in the separate hosts files DUT,TR,Server1 and Server2.
host_vars file for DUT is displayed below.
```
fanoutport:  "e101-027-0"
splitport:   "4x1"
speed:    "10g"
server_int:   "e101-027-1"
test_int1:   "e101-001-0"
test_int2:   "e101-002-0"
test_int3:   "e101-003-0"
test_mgmtint:   "eth0"
```
* `fanouport` is the port used in the remote switch to split the port ex. 40G to 4x10g
* `splitport` is to define how to split the port to ex.100G to 2x1(two 40G ports) o 4x1 (four 10G ports)
* `speed` is to define the speed of the split port
* `test_int1` is the first interface connecting from DUT to TR
* `test_int2` is the second interface connecting from DUT to TR
* `test_int3` is the third interface connecting from DUT to TR
* `test_mgmtint` is the management interface of DUT

# group_vars

group_vars is the common variable file across the roles which defines the service names,path and the image installation variables. File is displayed below.

```
---
log_cmd:        opx_logging_cli
path:           /usr/bin
service_cps:    opx-cps
service_pas:    opx-pas
service_nas:    opx-nas
service_acl:    opx-acl-init
service_qos:    opx-qos-init
system_status:  opx-show-system-status
show_env:       opx-show-env
show_media:     opx-show-transceivers
fanoutcmd:   "opx-config-fanout"
statsCommand:     "opx-show-stats"
switchShell:    "opx-switch-shell"
configSystem:    "opx-config-switch"
versionCommand:  "opx-show-version"
nameserver: "8.8.8.8"

#### OPX Image Installation Variables

telnet_esc: "^G"
telnet_close: "\x07c\n"
cmd: "pwd"
default_exp:
  '\[Enter .* to cli \]': "\n"
  BIOS initializations...: "{{ telnet_close }}"
cmds: "{{ cmd.splitlines() + [ telnet_close ] }}"
exp:
  'login: $': "{{ ansible_ssh_user }}"
  'assword.*: $': "{{ ansible_ssh_pass }}"
  '.*\$ $': "sudo -i"
  '.*\# $': "{{ cmds }}"
extra_exp: {}
nos_install_exp:
  Initializing installer: ""
  Installing OPX on primary partition: ""
  Updating database of manual pages: ""
  apt-get update: ""
  apt-get install: ""
  Synchronizing standby partition: ""
  Installation finished.: ""
  machine restart: ""

```

* `log_cmd` is the logging command to enable logs in the switch
* `path` defines the path for all the scripts in the switch
* `service_cps` defines the CPS service name
* `service_pas` defines the PAS service name
* `service_acl` defines the ACL service name
* `service_qos` defines the QoS service name
* `show_env` defines the command used to show the environment in remote switch
* `show_media` defines the command used to show the transceivers in remote switch
* `fanoutcmd` defines the fanout command used in remote switch to split the ports
* `statsCommand` defines the command to check the statistics of a port in remote switch
* `switchShell` defines the command used to check the hardware
* `configSystem` defines the command used to configure the switch hardware tables
* `versionCommand` defines the commnd used to check the image version of the switch
* `ansible_new_pass` is the new password configured in the switch
* `nameserver` defines the nameserver configurations for image installation
* `OPX Image Installation Variables` is to login to the switch, change password and configure the management IP 

