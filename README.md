## How to run Playbooks

Playbooks are located in playbook folder. By default, ansible selects the hosts file path from ansible.cfg file located in /etc/ansible folder. Change the hosts file path in ansible.cfg file to locate your hosts. Sample hosts file is displayed below. 

**Note**: *Image installation only works on hardware switches and not VM and VM has very limited functionality on L2*
### Image Installation
```
ansible-playbook playbook/site.yml -t "img_install" -e "http://archive.openswitch.net/installers/3.0.0-dev2/Dell-EMC/PKGS_OPX-3.0.0-dev2-installer-x86_64.bin" -vv
```
### Run L2 script
```
ansible-playbook playbook/site.yml -t "l2mac" -vv
```
### Run image installation and smoketest
```
ansible-playbook playbook/site.yml -t "img_install,smoketest"  -e "http://archive.openswitch.net/installers/3.0.0-dev2/Dell-EMC/PKGS_OPX-3.0.0-dev2-installer-x86_64.bin" -vv

-e = extra variable option to set image path
-t = tags to run
```
### Run image installation and l2mac script
```
ansible-playbook playbook/site.yml -t "img_install,l2mac" -vv
```
## Files needs to be modified for running against own Testbed

### hosts
hosts file needs to be modified with the corresponding switch Management IP address, username and password

```
[1host]

DUT ansible_host='<Mgmt-IP>' ansible_ssh_user='<username>' ansible_ssh_pass='<password>' ansible_sudo_pass='<sudo password>' 


[2host]

DUT ansible_host='<Mgmt-IP>' ansible_ssh_user='<username>' ansible_ssh_pass='<password>' ansible_sudo_pass='<sudo password>'
TR ansible_host='<Mgmt-IP>' ansible_ssh_user='<username>' ansible_ssh_pass='<password>' ansible_sudo_pass='<sudo password>' 
Server1 ansible_host='<Mgmt-IP>' ansible_ssh_user='<username>' ansible_ssh_pass='<password>' ansible_sudo_pass='<sudo password>'
Server2 ansible_host='<Mgmt-IP>' ansible_ssh_user='<username>' ansible_ssh_pass='<password>' ansible_sudo_pass='<sudo password>'   
```
**Note** : *DUT in 1host and 2host should have the same Management IP address*

### playbook/host_vars/DUT

```
ansible_console: '<consoleIP>'
console_port:  '<consolePort>'
ansible_host_gateway: '<MgmtGateway>'
```
