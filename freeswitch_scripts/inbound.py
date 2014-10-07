from freeswitch import *
import pprint
import MySQLdb


# Prototype

def handler(session,args):


	db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="ipsafe")
	cur = db.cursor() 

	session.execute("set","call_direction=inbound")
	session.execute("set","continue_on_fail=true")
	session.execute("set","hangup_after_bridge=true")

	consoleLog('info', '>>> Starting Inbound Call\n')
	consoleLog('info', '> Source: %s\n' % session.getVariable("source"))
	consoleLog('info', '> Destination: %s\n' % session.getVariable("destination_number"))
	consoleLog('info', '> Context: %s\n' % session.getVariable("context"))
	consoleLog('info', '> CLID: %s\n' % session.getVariable("caller_id_name"))
	consoleLog('info', '> CLID Number: %s\n' % session.getVariable("caller_id_number"))
	consoleLog('info', '> Channel: %s\n' % session.getVariable("channel_name"))
	consoleLog('info', '> UniqueID: %s\n' % session.getVariable("uuid"))
	consoleLog('info', '> direction: %s\n' % session.getVariable("direction"))
	consoleLog('info', '> Session ID: %s\n' % session.getVariable("session_id"))
	consoleLog('info', '> Received IP: %s\n' % session.getVariable("sip_received_ip"))
	consoleLog('info', '> ACL Authed IP: %s\n' % session.getVariable("sip_acl_authed_by"))
	consoleLog('info', '> Network IP: %s\n' % session.getVariable("sip_network_ip"))
	consoleLog('info', '> Auth ACL: %s\n' % session.getVariable("auth_acl"))
	consoleLog('info', '> User Agent: %s\n' % session.getVariable("sip_user_agent"))
	consoleLog('info', '> VMD: %s\n' % session.getVariable("vmd"))

	session.answer()
	#session.setHangupHook(hangup_hook)
	#session.setInputCallback(input_callback)



	sql = ('''SELECT destination FROM inbound_rules 
			INNER JOIN inbound_routes ON inbound_routes_id = inbound_routes.id 
			WHERE weekdays LIKE CONCAT('%%', DATE_FORMAT(NOW(), '%%w'), '%%') 
    		AND CURTIME() BETWEEN start AND stop
    		AND did = '%s' LIMIT 1''' % session.getVariable("destination_number"))

	consoleLog('info', '> SQL Inbound: %s\n' % sql)
	res = cur.execute(sql)
	if (res):
		for row in cur.fetchone():
			dial_string = "user/%s" % row
			consoleLog('info', '> Dial string: %s\n' % dial_string)
			session.execute("bridge", dial_string)
	else:
 		session.execute("set", "hangup_commentary=Not found inbound routes")
 		consoleLog('info', '> Not found inbound routes to did %s\n' % session.getVariable("destination_number"))
 		session.hangup()