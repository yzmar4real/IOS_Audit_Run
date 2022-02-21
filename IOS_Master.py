import sys
import time
import logging
import json
import csv
from genie.testbed import load
from pyats.log.utils import banner
from IOS_MasterFunction import intf_func,arp_func,ver_func,cdp_func, mac_func, etherchannel_func, intf_brief_func, intf_status_func

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
log = logging.getLogger()

log.info(banner("LOADING TESTBED FILES"))
testbed = load('genie.yml')
log.info("\nPASS: Successfully loaded testbed '{}'\n".format(testbed.name))

######## Defining the list of commands to perform and storing them in specific arrays ########

log.info(banner("CREATING ARRAY STORE FOR COMMAND OUTPUTS"))

command = ['show run', 'show version', 'show interfaces status', 'show ip arp', 'show cdp neighbor detail', 'show mac address-table', 'show etherchannel summary', 'show ip int brief', 'show interfaces description']
special = {'show version', 'show interfaces status', 'show ip arp', 'show cdp neighbor detail', 'show mac address-table', 'show etherchannel summary', 'show ip int brief', 'show interfaces description'}

Device_Store = []
Intf_Store = []
Arp_Store = []
Cdp_Store = []
Mac_Store = []
Etherchannel_Store = []
Intf_Brief_Store = []
Intf_Status_Store = []

######## Defining header lists for information to be stored within the csv files under each category ########

log.info(banner("CREATING CSV FILE REFERENCE LISTS"))

device_names = ['Switch', 'Version', 'Image', 'Model', 'Memory', 'License', 'Serial Number']
interface_names = ['Switch', 'Description', 'Status', 'VLAN', 'DUPLEX', 'SPEED','PORT TYPE']
arp_names = ['Switch', 'IP', 'MAC', 'INTERFACE', 'ORIGIN', 'AGE']
cdp_names = ['Switch', 'REMOTE_DEVICE', 'REMOTE_NATIVEVLAN','REMOTE_DEVICE_MGTIP','REMOTE_PORT', 'LOCAL_PORT']
mac_names = ["Switch","MAC_ADDRESS", "MAC_TYPE", "MAC_VLAN", "MAC_PORT"]
etherchannel_names = ["Switch", "CHANNEL_LAGS", "CHANNEL_AGG", "CHANNEL_NAME", "CHANNEL_ID", "CHANNEL_STATUS", "CHANNEL_MEMBERS", "CHANNEL_FLAGS"]
intf_brief_names = ["Switch","INTERFACE_NAME", "IP_ADDRESS", "INTERFACE_STATUS"]
intf_desc_names = ["Switch","INTERFACE","Description", "Status", "PROTOCOL"]

log.info("\nPASS: Successfully created CSV Lists \n")

########## Defining output csv file names for each output category

log.info(banner("CREATING CSV FILES"))

csv_file = "Device.csv"
csv_file = "Interface.csv"
csv_file = "Arp.csv"
csv_file = "cdp.csv"
csv_file = "mac.csv"
csv_file = "etherchannel.csv"
csv_file = "intf_brief.csv"
csv_file = "intf_desc.csv"

log.info("\nPASS: Successfully created CSV files \n")

for device in testbed:
    
    try:
        device.connect(learn_hostname=True,init_exec_commands=[],init_config_commands=[],log_stdout=True)
    except ConnectionError:
        print('----- ERROR -----')
        print(f" Cannot connect to {device.connections.vty.ip}")
        continue

##### Raw output storage ######
    
    for command in command:
        try:
            output = device.execute(command)
            
            with open(device.alias+'Output.txt', 'a') as f:
                f.write('\n\n ########## ' + str(command) + ' ' + '########################## \n\n')
                f.write(str(output)) 
                     
        except Exception as e:
            with open(device.alias+'Exception.txt', 'a') as f:
                f.write('\n\n ########## ' + str(e) + ' ' + '########################## \n\n')

#################################################################################################
    log.info(banner("EXTRACTING AUDIT INFORMATION"))

    for special in special:
        if special == 'show version':
            try:
                special_output = device.parse(special)
                Device_Store = ver_func(special_output,device)
            except Exception as e:
                with open(device.alias+'Exception.txt', 'a') as f:
                    f.write('\n\n ########## ' + str(e) + ' ' + '########################## \n\n')
                Device_Store = [{"Switch": device.alias, "Version": 'N/A', "Image": 'N/A', "Model": 'N/A', "Memory": 'N/A', "License": 'N/A', "Serial Number": 'N/A'}] 
        
        if special == 'show interfaces description':
            try:
                intf_desc = device.parse(special)
                Intf_Store = intf_func(intf_desc,device)               
            except Exception as e:
                with open(device.alias+'Exception.txt', 'a') as f:
                    f.write('\n\n ########## ' + str(e) + ' ' + '########################## \n\n')
                Intf_Store = [{"Switch": device.alias, "INTERFACE": 'N/A', "Description": 'N/A', "Status": 'N/A', "PROTOCOL": 'N/A'}]

        if special == 'show ip arp':
            try:
                arp = device.parse(special)
                Arp_Store = arp_func(arp,device)               
            except Exception as e:
                with open(device.alias+'Exception.txt', 'a') as f:
                    f.write('\n\n ########## ' + str(e) + ' ' + '########################## \n\n')
                Arp_Store = [{"Switch": device.alias, "IP": 'N/A', "MAC": 'N/A', "INTERFACE": 'N/A', "ORIGIN": 'N/A', "AGE": 'N/A'}]
                
        if special == 'show cdp neighbor detail':
            try:
                cdp_nei = device.parse(special)
                Cdp_Store = cdp_func(cdp_nei,device)               
            except Exception as e:
                with open(device.alias+'Exception.txt', 'a') as f:
                    f.write('\n\n ########## ' + str(e) + ' ' + '########################## \n\n')
                Cdp_Store = [{"Switch": device.alias, "REMOTE_DEVICE": 'N/A', "REMOTE_NATIVEVLAN": 'N/A', "REMOTE_DEVICE_MGTIP": 'N/A', "REMOTE_PORT": 'N/A', "LOCAL_PORT": 'N/A'}]

        if special == 'show mac address-table':
            try:
                mac = device.parse(special)
                Mac_Store = mac_func(mac,device)               
            except Exception as e:
                with open(device.alias+'Exception.txt', 'a') as f:
                    f.write('\n\n ########## ' + str(e) + ' ' + '########################## \n\n')
                Mac_Store = [{"Switch": device.alias, "MAC_ADDRESS": 'N/A', "MAC_TYPE": 'N/A', "MAC_VLAN": 'N/A', "MAC_PORT": 'N/A'}]

        if special == 'show etherchannel summary':
            try:
                port_channel = device.parse(special)
                Etherchannel_Store = etherchannel_func(port_channel,device)               
            except Exception as e:
                with open(device.alias+'Exception.txt', 'a') as f:
                    f.write('\n\n ########## ' + str(e) + ' ' + '########################## \n\n')
                Etherchannel_Store = [{"Switch": device.alias, "CHANNEL_LAGS": 'N/A', "CHANNEL_AGG": 'N/A', "CHANNEL_NAME": 'N/A', "CHANNEL_ID": 'N/A', "CHANNEL_STATUS": 'N/A', "CHANNEL_MEMBERS": 'N/A', "CHANNEL_FLAGS": 'N/A'}]

        if special == 'show ip int brief':
            try:
                intf_brief = device.parse(special)
                Intf_Brief_Store = intf_brief_func(intf_brief,device)               
            except Exception as e:
                with open(device.alias+'Exception.txt', 'a') as f:
                    f.write('\n\n ########## ' + str(e) + ' ' + '########################## \n\n')
                Intf_Brief_Store = [{"Switch": device.alias, "INTERFACE_NAME": 'N/A', "IP_ADDRESS": 'N/A', "INTERFACE_STATUS": 'N/A'}]

        if special == 'show interfaces status':
            try:
                intf_status = device.parse(special)
                Intf_Status_Store = intf_status_func(intf_status,device)               
            except Exception as e:
                with open(device.alias+'Exception.txt', 'a') as f:
                    f.write('\n\n ########## ' + str(e) + ' ' + '########################## \n\n')
                Intf_Status_Store = [{"Switch": device.alias, "Description": 'N/A', "Status": 'N/A', "VLAN": 'N/A', "DUPLEX": 'N/A', "SPEED": 'N/A', "PORT TYPE": 'N/A'}]
 
with open('Device.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames= device_names)
    writer.writeheader()
    writer.writerows(Device_Store)

with open('Interface.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames= interface_names)
    writer.writeheader()
    writer.writerows(Intf_Status_Store)
    
with open('Arp.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames= arp_names)
    writer.writeheader()
    writer.writerows(Arp_Store)

with open('cdp.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames= cdp_names)
    writer.writeheader()
    writer.writerows(Cdp_Store)

with open('mac.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames= mac_names)
    writer.writeheader()
    writer.writerows(Mac_Store)

with open('etherchannel.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames= etherchannel_names)
    writer.writeheader()
    writer.writerows(Etherchannel_Store)

with open('intf_brief.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames= intf_brief_names)
    writer.writeheader()
    writer.writerows(Intf_Brief_Store)
    
with open('intf_desc.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames= intf_desc_names)
    writer.writeheader()
    writer.writerows(Intf_Store)
