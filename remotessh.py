from netmiko import ConnectHandler

f = open('D:\Programming\infovlans.txt','w')
Ciscodevice = {
	'device_type':'cisco_ios',
	'ip':'10.112.144.93',
	'username':'xxxxxxx',
	'password':'xxxxxxx',
}

connection = ConnectHandler(**Ciscodevice)
output = connection.send_command('show vlan brief')
output = output.split()
count = 0
vlans = []


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
#Función para saber si la cadena puede ser transformada en un entero

for i in output:
	if RepresentsInt(i)==True:
		vlans.append(count)
		vlans.append(output[output.index(i)+1])
		count = 0
	if i.startswith('Gi') or i.startswith('Fa'):
		count = count+1
#Agrega valor de vlan anterior 
#y el nomber de la proxima vlan a vlans si el valor leido es un entero
#si el valor de i empieza con Gi o Fa, el valor de count incrementa en 1

f.write('{:<25} {}'.format('Nombre de Vlan','Puertos en Vlan \n'))

vlans.remove(0)
vlans.pop()

for i in vlans:
	if (vlans.index(i)+1) % 2 == 0:
		f.write( ' '+ str(i) + '\n')
	else:
		f.write('{:<30}'.format(str(i)))

f.close()
f = open('D:\Programming\infovlans.txt','r+')
output = f.readlines()
f.seek(0)

for line in output:
	if '0\n' not in line:
		f.write(line)
#Elimina Vlans que no tengan un PC

f.truncate()
f.close()
