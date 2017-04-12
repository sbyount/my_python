from netmiko import ConnectHandler

# define device_type
cisco_3945 = {
    'device_type': 'cisco_ios',
    'ip':   '10.192.65.180',
    'username': 'netsupport',
    'password': 'whyohwhy',
    'port' : 8022,          # optional, defaults to 22
    'secret': 'secret',     # optional, defaults to ''
    'verbose': False,       # optional, defaults to False
}
# pass in device dictionary, establish ssh session
net_connect = ConnectHandler(**cisco_3945)

output = net_connect.send_command('show ip int brief')
print(output
