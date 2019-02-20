# Role Name

This role is used for image installation.

# Requirements

The prerequisite for this role is to have Dell hardware switch with ONIE bootloader.

# Role Variables

The role variable file is defined in vars/main.yml. The file and the description of each variable is defined below.

```
set_eth0: |
  grep -q -F 'source-directory /etc/network/interfaces.d' /etc/network/interfaces || echo 'source-directory /etc/network/interfaces.d' >> /etc/network/interfaces
  grep -q -F 'nameserver' /etc/resolv.conf || echo 'nameserver {{nameserver}}' >> /etc/resolv.conf
  ifconfig eth0 | grep 'addr:{{ ansible_host }}' || ifconfig eth0 {{ ansible_host }} netmask {{ ansible_host_netmask }} up
  ifconfig eth0
  route add default gateway {{ ansible_host_gateway }}
  route -n
  service networking restart
  ifconfig eth0 {{ ansible_host }} netmask {{ ansible_host_netmask }} up
  ip route add default via {{ ansible_host_gateway }}
  ifconfig eth0
grub_boot_onie: |
  ln -sf /mnt/boot/grub /boot/grub
  grub-reboot $(( $( grep menuentry /boot/grub/grub.cfg | grep -n ONIE | cut -d: -f 1 ) - 1 ))
get_onie_prompt:
  'Info: ': "onie-discovery-stop"
  'ONIE:/ #': "\x07c\n"
set_onie_eth0: |
  onie-discovery-stop
  sleep 3
  ps | grep {networking.sh} | awk '{print $1}' | xargs kill -9
  sleep 3
  echo 'nameserver 8.8.8.8' > /etc/resolv.conf
  ifconfig eth0 {{ ansible_host }} netmask {{ ansible_host_netmask }} up
  route add default gateway {{ ansible_host_gateway }}
  ifconfig eth0
  ip route add default via {{ ansible_host_gateway }}
  route -n
nos_install: |
  onie-nos-install {{ image|default('http://archive.openswitch.net/installers/3.0.0-dev2/Dell-EMC/PKGS_OPX-3.0.0-dev2-installer-x86_64.bin') }}
```

* `set_eth0` defines the commands used for setting the management IP,default gateway and nameserver configurations after the image installation
* `grub_boot_onie` defines the commands used to bring the switch to ONIE prompt 
* `get_onie_prompt` defines the command used to stop th DHCP discovery process in ONIE
* `set_onie_eth0` defines the commands used for setting the management IP,default gateway and nameserver configurations in ONIE
* `nos_install` defines the command used to install the NOS(image) on to the switch

# Dependencies

Hardware switch with ONIE bootloader

# Example Playbook

all is mentioned in hosts. -l option is used in command line to limit the image installation to DUT and TR

```
- hosts: all
  gather_facts: false
  pre_tasks:
    - setup:
  become: false
  roles:
    - {role: General/roles/img_install, tags: ['always','img_install'], when: image is defined}
```
# License

BSD

# Author Information

Madhusudhanan Santhanam - santhanam_madhusudha@dell.com
