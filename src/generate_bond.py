#! /usr/bin/python

import csv
import sys
import os
import collections


def read(path):
    content_dict = {}

    if not os.path.exists(path):
        return content_dict

    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line:
                idx = line.index('=')
                key = line[0:idx].strip()
                value = line[idx+1:].strip()
                content_dict[key] = value
    return content_dict


def write(path, data):
    content = ''
    for k,v in data.items():
        content += '{0}={1}\n'.format(k,v)
    
    with open(path, 'w') as f:
        f.write(content)


ifcfg_prefix = 'ifcfg-'


if __name__ == '__main__':
    input = str(sys.argv[1])
    
    with open(input) as csvfile:
        fieldnames = ["SERIAL_NUMBER", "PXE_IP", "HOSTNAME",\
                    "ADMIN_NAME", "ADMIN_IP", "ADMIN_INTERFACE", \
                    "PUBLIC_NAME", "PUBLIC_IP", "PUBLIC_INTERFACE", \
                    "PRIVATE_NAME", "PRIVATE_IP", "PRIVATE_INTERFACE", \
                    "STORAGE_NAME", "STORAGE_IP", "STORAGE_INTERFACE"]
        reader = csv.DictReader(csvfile,fieldnames=fieldnames)
        
        header = next(reader)
        for row in reader:
            for net_type in ['ADMIN', 'PRIVATE', 'STORAGE', 'PUBLIC']:            
                bond_header = net_type + '_NAME'
                bond_name = row[bond_header]
                if not bond_name:
                    continue
                
                suffix = net_type.lower()
                dir_path = os.path.join('/tmp/', row['ADMIN_IP'], suffix)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path) 
                    
                ip_header = net_type + '_IP'
                bond_ip = row[ip_header]
                interface_header = net_type + '_INTERFACE'
                bond_interfaces = row[interface_header].split(',') 
                
                for ifname in bond_interfaces:
                    if not ifname:
                        continue
    
                    if_path = os.path.join(dir_path, ifcfg_prefix+ifname)
                    
                    '''
                    DEVICE=eth0
                    TYPE=Ethernet
                    BOOTPROTO=none
                    ONBOOT=yes
                    MASTER=bond0
                    SLAVE=yes
                    NM_CONTROLLED=no
                    '''
                    eth_data = collections.OrderedDict()
                    eth_data['TYPE'] = 'Ethernet'
                    eth_data['BOOTPROTO'] = 'none'
                    eth_data['ONBOOT'] = 'yes'
                    eth_data['NM_CONTROLLED'] = 'no'
                    eth_data['SLAVE'] = 'yes'

                    eth_data['DEVICE'] = ifname
                    eth_data['MASTER'] = bond_name.split('.')[0]
                    write(if_path, eth_data) 
                
                bond_vlan = bond_name.find('.') > 0
                bond_data = collections.OrderedDict()
                '''
                NAME=bond0
                DEVICE=bond0
                
                BOOTPROTO=none
                ONBOOT=yes
                USERCTL=no
                TYPE=Bond
                BONDING_MASTER=yes
                NM_CONTROLLED=no
                
                IPADDR=192.168.1.10
                NETMASK=255.255.255.0
                BONDING_OPTS="mode=active-backup miimon=100"
                '''
                bond_data['NAME'] = bond_name
                bond_data['DEVICE'] = bond_name                
                bond_data['TYPE'] = 'Bond'
                bond_data['BONDING_MASTER'] = 'yes'
                
                bond_data['ONBOOT'] = 'yes'
                bond_data['USERCTL'] = 'no'
                bond_data['NM_CONTROLLED'] = 'no'
                bond_data['IPADDR'] = bond_ip
                bond_data['BOOTPROTO'] = 'none'
                
                default_bond = read('/etc/bond-util/bond_'+suffix) 
                bond_data.update(default_bond)

                if bond_vlan:
                    '''
                    DEVICE=bond0.100
                    NAME=bond0.100
                    BOOTPROTO=none
                    ONBOOT=yes
                    USERCTL=no
                    VLAN=yes
                    TYPE=Bond
                    NM_CONTROLLED=no
                    IPADDR=192.168.1.10
                    NETMASK=255.255.255.0
                    '''
                    # generate bond vlan file first.
                    bond_data['VLAN'] = 'yes'
                    bond_data['ONPARENT'] = 'yes'

                    # write vlan file
                    opts = bond_data.pop('BONDING_OPTS')
                    bmaster = bond_data.pop('BONDING_MASTER')

                    bond_path = os.path.join(dir_path, ifcfg_prefix+bond_name)
                    write(bond_path, bond_data)
                    
                    #write bond file
                    bname = bond_name.split('.')[0] 
                    bond_data['NAME'] = bname
                    bond_data['DEVICE'] = bname
                    for k in ['IPADDR', 'NETMASK', 'GATEWAY', 'VLAN']:
                        if k in bond_data:
                            bond_data.pop(k)
                    bond_data['BONDING_OPTS'] = opts
                    bond_data['BONDING_MASTER'] = bmaster
                    bond_path = os.path.join(dir_path, ifcfg_prefix+bname)
                    write(bond_path, bond_data)
                else:
                    bond_path = os.path.join(dir_path, ifcfg_prefix+bond_name)
                    write(bond_path, bond_data)
  
