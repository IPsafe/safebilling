#!/usr/bin/env python
# -*- coding: utf-8 -*-
from email.header    import Header
from email.mime.text import MIMEText
from smtplib         import SMTP_SSL
import subprocess
import traceback
import socket


def mail():
	try:
		hdd_use = subprocess.check_output("df -lh / | grep '% /' | cut -d 'G' -f4 | cut -d '%' -f1", shell=True).split()[0]
		#print 'Uso de disco: %s' % str(hdd_use)

		if float(hdd_use) < 75:
			return False

		ipaddr = socket.gethostbyname(socket.getfqdn())
		#print 'IP : %s' % str(ipaddr)

		df = subprocess.check_output("df -h", shell=True)

		mail_body = '''
		Monitor de Disco.

		Uso de Disco: %s%%
		IP: %s

		Informacoes:
		%s
				''' % (str(hdd_use), str(ipaddr), str(df))

		# SMTP
		
		login, password = 'suporte@ipsafe.com.br', '_ipsafe@Suporte'
		mail_header = '[ALERTA] Monitor de Disco - %s%% (%s)' % (str(hdd_use), str(ipaddr))
		msg = MIMEText(mail_body, 'plain', 'utf-8')
		msg['Subject'] = Header(mail_header, 'utf-8')
		msg['From'] = login
		msg['To'] = 'engenharia@ipsafe.com.br'

		# send it via gmail
		s = SMTP_SSL('smtp.gmail.com', 465, timeout=10)
		s.set_debuglevel(1)
		try:
		    s.login(login, password)
		    s.sendmail(msg['From'], msg['To'], msg.as_string())

		finally:
			s.quit()

	except Exception,e:
		traceback.print_exc()


if __name__ == '__main__':
    try:
        mail()
    except:
	print 'Falha ao executar'
        raise

