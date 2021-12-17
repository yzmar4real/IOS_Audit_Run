intf_desc_Store = []
Device_Store = []
Arp_Store = []
cdp_Store = []
mac_Store = []
etherchannel_Store = []
pc_member = []
pc_flags = []
intf_brief_Store = []
intf_status_Store = []
  
def ver_func(special_output,device):
                    
    sys_version = special_output['version']['version']
    sys_image = special_output['version']['system_image']
    sys_model = special_output['version']['chassis']
    sys_memory = special_output['version']['main_mem']
    
    sys_lic = special_output['version']['license_level']
    #sys_lic = 'N/A'
    sys_serial = special_output['version']['chassis_sn']                    
                    
    Device_Audit = {"Switch": device.alias, "Version": sys_version, "Image": sys_image, "Model": sys_model, "Memory": sys_memory, "License": sys_lic, "Serial Number": sys_serial}                   
    Device_Store.append(Device_Audit)                
    return Device_Store

if __name__ == "__main__": 
    ver_func()()       

def intf_func(intf_desc,device):
      
    for intf in intf_desc['interfaces'].keys():
        intf_desc_port = intf
        intf_desc_name = intf_desc['interfaces'][intf]['description']
        intf_desc_status = intf_desc['interfaces'][intf]['status']
        intf_desc_protocol = intf_desc['interfaces'][intf]['protocol']
        intf_desc_Audit = {"Switch": device.alias, "INTERFACE": intf_desc_port, "Description": intf_desc_name, "Status": intf_desc_status, "PROTOCOL": intf_desc_protocol}
        intf_desc_Store.append(intf_desc_Audit) 
    return intf_desc_Store

if __name__ == "__main__": 
    intf_func()
            
def arp_func(arp,device):    
    
    for intf in arp['interfaces'].keys():
        for arp_intf in arp['interfaces'][intf]['ipv4']['neighbors'].keys():
            arp_ip = arp['interfaces'][intf]['ipv4']['neighbors'][arp_intf]['ip']
            arp_mac = arp['interfaces'][intf]['ipv4']['neighbors'][arp_intf]['link_layer_address']
            arp_type = arp['interfaces'][intf]['ipv4']['neighbors'][arp_intf]['type']
            arp_origin = arp['interfaces'][intf]['ipv4']['neighbors'][arp_intf]['origin']
            arp_age = arp['interfaces'][intf]['ipv4']['neighbors'][arp_intf]['age']

            Arp_Audit = {"Switch": device.alias, "IP": arp_ip, "MAC": arp_mac, "INTERFACE": arp_type, "ORIGIN": arp_origin, "AGE": arp_age}
            Arp_Store.append(Arp_Audit)
    return Arp_Store
    
                
if __name__ == "__main__": 
    arp_func()
    
    
def cdp_func(cdp_nei,device): 

    j = 1
    while j < len(cdp_nei['index'].keys()):
        cdp_remote_device = cdp_nei['index'][j]['device_id'] 
        cdp_remote_nativevlan = print(cdp_nei['index'][j]['native_vlan'])   
        cdp_remote_mgtip = cdp_nei['index'][j]['management_addresses']
        cdp_remote_port = cdp_nei['index'][j]['port_id']
        cdp_local_port = cdp_nei['index'][j]['local_interface']
        j+=1     

        cdp_Audit = {"Switch": device.alias, "REMOTE_DEVICE": cdp_remote_device, "REMOTE_NATIVEVLAN": cdp_remote_nativevlan, "REMOTE_DEVICE_MGTIP": cdp_remote_mgtip, "REMOTE_PORT": cdp_remote_port, "LOCAL_PORT": cdp_local_port}
        cdp_Store.append(cdp_Audit)
    return cdp_Store

if __name__ == "__main__": 
    cdp_func()
    
    
def mac_func(mac,device):  
    
    for mac_int in mac['mac_table']['vlans'].keys():
        mac_vlan = mac['mac_table']['vlans'][mac_int]['vlan']
        for mac_add in mac['mac_table']['vlans'][mac_int]['mac_addresses'].keys():
            mac_hwadd = mac['mac_table']['vlans'][mac_int]['mac_addresses'][mac_add]['mac_address']
            for interface in mac['mac_table']['vlans'][mac_int]['mac_addresses'][mac_add]['interfaces'].keys():
                mac_port = mac['mac_table']['vlans'][mac_int]['mac_addresses'][mac_add]['interfaces'][interface]['interface']
                mac_type = mac['mac_table']['vlans'][mac_int]['mac_addresses'][mac_add]['interfaces'][interface]['entry_type']    

                mac_Audit = {"Switch": device.alias, "MAC_ADDRESS": mac_hwadd, "MAC_TYPE": mac_type, "MAC_VLAN": mac_vlan, "MAC_PORT": mac_port}
                mac_Store.append(mac_Audit)

    return mac_Store

if __name__ == "__main__": 
    mac_func()    
    
        
def etherchannel_func(port_channel,device):
    portchannel_lags = port_channel['number_of_lag_in_use']
    portchannel_agg = port_channel['number_of_aggregators']
    for port_intf in port_channel['interfaces'].keys():
        portchannel_name = port_channel['interfaces'][port_intf]['name']
        portchannel_id = port_channel['interfaces'][port_intf]['bundle_id']
        portchannel_operstatus = port_channel['interfaces'][port_intf]['oper_status']
        for member in port_channel['interfaces'][port_intf]['members'].keys():
            pc_member.append(member)
            pc_flags.append(port_channel['interfaces'][port_intf]['members'][member]['flags'])
        portchannel_flags = pc_flags
        portchannel_members = pc_member

        etherchannel_Audit = {"Switch": device.alias, "CHANNEL_LAGS": portchannel_lags, "CHANNEL_AGG": portchannel_agg, "CHANNEL_NAME": portchannel_name, "CHANNEL_ID": portchannel_id, "CHANNEL_STATUS": portchannel_operstatus, "CHANNEL_MEMBERS":portchannel_members, "CHANNEL_FLAGS": portchannel_flags}
        etherchannel_Store.append(etherchannel_Audit) 

    return etherchannel_Store
if __name__ == "__main__": 
    etherchannel_func() 


def intf_brief_func(intf_brief,device):
    for set in intf_brief['interface'].keys():
        if 'vlan_id' in intf_brief['interface'][set].keys():
            for key in intf_brief['interface'][set]['vlan_id']:
                intfb_name = set
                intfb_ip = intf_brief['interface'][set]['vlan_id'][key]['ip_address']
                intfb_status = intf_brief['interface'][set]['vlan_id'][key]['status']
        elif 'ip_address' in intf_brief['interface'][set].keys():
            intfb_name = set
            intfb_ip = intf_brief['interface'][set]['ip_address']
            intfb_status = intf_brief['interface'][set]['status']
              
        intf_brief_Audit = {"Switch": device.alias, "INTERFACE_NAME": intfb_name, "IP_ADDRESS": intfb_ip, "INTERFACE_STATUS": intfb_status}
        intf_brief_Store.append(intf_brief_Audit)

    return intf_brief_Store
if __name__ == "__main__": 
    intf_brief_func()
    

def intf_status_func(intf_status,device):
    for intf in intf_status['interfaces'].keys():
        if 'name' in intf_status['interfaces'][intf].keys():
            intfa_desc = intf_status['interfaces'][intf]['name']
            intfa_status = intf_status['interfaces'][intf]['status']
            intfa_vlan = intf_status['interfaces'][intf]['vlan']
            intfa_duplex = intf_status['interfaces'][intf]['duplex_code']
            intfa_speed = intf_status['interfaces'][intf]['port_speed']
            intfa_type = intf_status['interfaces'][intf]['type']
        
        elif 'type' in intf_status['interfaces'][intf].keys():
            intfa_desc = 'N/A'
            intfa_status = intf_status['interfaces'][intf]['status']
            intfa_vlan = intf_status['interfaces'][intf]['vlan']
            intfa_duplex = intf_status['interfaces'][intf]['duplex_code']
            intfa_speed = intf_status['interfaces'][intf]['port_speed']
            intfa_type = intf_status['interfaces'][intf]['type']
        
        else:
            intfa_desc = 'N/A'
            intfa_status = intf_status['interfaces'][intf]['status']
            intfa_vlan = intf_status['interfaces'][intf]['vlan']
            intfa_duplex = intf_status['interfaces'][intf]['duplex_code']
            intfa_speed = intf_status['interfaces'][intf]['port_speed']
            intfa_type = 'N/A'
    
        Intf_Status_Audit = {"Switch": device.alias, "Description": intfa_desc, "Status": intfa_status, "VLAN": intfa_vlan, "DUPLEX": intfa_duplex, "SPEED": intfa_speed, "PORT TYPE": intfa_type}
        intf_status_Store.append(Intf_Status_Audit)

    return intf_status_Store
if __name__ == "__main__": 
    intf_status_func()