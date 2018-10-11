## opx-test-infra
The opx-test-infra app is built to make it easy to run test suites. On GUI you can select set of tests to run (sanity or full or individual playbooks), update and modify test suite files and run Jenkins. The GUI automatically creates and runs Jenkins jobs and emails the result.

Test Infrastructure mainly comprises of Ansible Playbooks (to define test cases), GUI (a flask based app) and Jenkins (to run ansible jobs) 

![image](https://user-images.githubusercontent.com/14809064/46828984-56f8ef80-cd51-11e8-9918-9c2aecc7c2b9.png)

## How to set up the enviroment for opx-test-infra 
[setup.sh](./setup.sh) script: Is used to setup the enviroment required by opx-test-infra. The script create a new user jenkins, install Jenkins, install required Jenkins plugins, update jenkins file to skip inital setup, start jenkins service, install Ansible, clone the opx-test ansible playbooks, install Flask and run the GUI on port 80. 
Clone the script and run:
```
sudo ./setup.sh
```
To access the opx-test-infra GUI, on your machine go to home/jenkins/jenkins/Unified-Test-Application folder and run:
```
python ut-app.py
```
View the GUI:
```
http://127.0.0.1 or http://mgmt-ip
```
To learn more about the opx-test-infra GUI refer: [README.md](./jenkins/Unified-Test-Application/README.md)

To access Jenkins GUI:
Ensure jenkins service is running:
```
service jenkins status
```
View the Jenkins GUI:
```
http://127.0.0.1:8080 or http://mgmt-ip:8080
```
Login in to jenkins using admin/admin

## How to manually run Playbooks without using GUI
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


(c) 2018 Dell Inc. or its subsidiaries. All Rights Reserved.
