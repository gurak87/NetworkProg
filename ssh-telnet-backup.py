from getpass import getpass
from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException
from netmiko.ssh_exception import  AuthenticationException
import telnetlib
import datetime

file = open('ipsfashions.txt')

user = input("Enter your Username: ")
password = getpass('Enter password: ')
enable = getpass('Enter enable password: ')


for device in file:
    try:
        #Intento de conexion por SSH
        gw = {'device_type': 'cisco_ios',
            'ip': device,
            'username': user,
            'password': password,
            'secret':enable,
            'fast_cli': False
            }
    
        net_connect = ConnectHandler(**gw)
        net_connect.enable()
        #proxima linea obtiene nombre del equipo
        hostname = net_connect.find_prompt()
        #Crea archivo de backup con nombre de equipo + fecha del dia
        with open (hostname[:-1]+'_'+str(datetime.date.today())+'.txt','w') as backup:
            backup.write(net_connect.send_command("show run",expect_string=hostname,delay_factor = 3).replace('\\n','\n'))
        net_connect.disconnect()
        print ('{:<30} {:<20} {:>15}'.format(hostname.replace('#',''), device.replace('\n', ''), 'respaldo OK - SSH'))
    except NetmikoTimeoutException:
        #SSH no habilitado en equipo, se intenta conectar por telnet
        tn = telnetlib.Telnet(device.replace('\n',''))
        tn.read_until(b"Username:")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password:")
            tn.write(password.encode('ascii') + b"\n")		
        tn.read_until(b"#")
        tn.write(b" terminal len 0\n")
        tn.read_until(b"#")
        #proximas 4 lineas obtienen nombre del equipo
        tn.write(b" show hostname\n")
        hostname = tn.read_until(b"#", timeout=5).decode("utf-8")
        hostname.replace("\r\n", "\n")
        hostname = hostname.split()[-1]
        result=''
        tn.write(b" show run\n")
        result = tn.read_until(b"#", timeout=5).decode("utf-8")
        #Crea archivo de backup con nombre de equipo + fecha del dia
        with open (hostname[:-1]+'_'+str(datetime.date.today())+'.txt','w') as backup:
            backup.write(result.replace("\r\n", "\n"))
        tn.write(b" exit\n")
        tn.close()
        print ('{:<30} {:<20} {:>15}'.format(hostname.replace('#',''), device.replace('\n', ''), 'respaldo OK - Telnet'))
    except AuthenticationException:
        print ('Bad Credentials - ' + device)



file.close()        