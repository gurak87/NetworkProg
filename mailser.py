from jumpssh import SSHSession
import time
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#As many fields as services needed, composed of binaries
mailser = [0]
i = 0

#Connect to mail server and account and give form to the message to be sent
def sendm (text):
	msg = MIMEMultipart()
	msg["Subject"] = 'Notificación de Conmutación' 
	msg["From"] = 'origin_mail'
	msg["To"] = 'target_mail'
	server = smtplib.SMTP_SSL('mail_server', server_port)
	server.login('origin_mail' ,'password')
	body = MIMEText(text)
	msg.attach(body)
	server.sendmail(msg["From"], msg["To"], msg.as_string())
	server.quit()

#Function determines if virtual MAC address from HSRP is where it should be
def hsrploc (service, mac, mail, port, remote):
	result = remote.get_cmd_output('show mac add int ' + port).split()
	if mac in result and mail == 0:
		return mail
	elif mac in result and mail == 1:
		#Sends mail with affected service and message of failover if mac returns to main site
		sendm(service + ' message')
		return 0
	elif mac not in result and mail == 1:
		return mail
	elif mac not in result and mail == 0:
		#Sends mail with affected service and message of failover if mac goes to backup site
		sendm(service + ' message')
		return 1
		
while True:
	try:
		#connect to gateway server
		gw = SSHSession(gw_server, 'username', password='password').open()
		#connect to remote device from gw server
		remote = gw.get_remote_session(remote_device, username='username', password='password')	
		#change field where service is located, used to determine if mail should be sent
		mailser[0] = hsrploc('service_name', 'mac_address', mailser[0], 'interface_id', remote) 
		#close remote device connection
		remote.close()
		i += 1
		print ('Check #', i)
		
		#close remote device and gw connection
		remote.close()		
		gw.close()
		
		#Waits 15 mins to check again
		time.sleep(60 * 15)
	except KeyboardInterrupt:
		print ('Interrupting Script')
		sys.exit(0)