from plivo.core.freeswitch.outboundsocket import OutboundEventSocket, OutboundServer
from urllib2 import urlopen
import json
import contextlib

from plivo.utils.logger import StdoutLogger, FileLogger
import gevent
from gevent.queue import Queue
from gevent import monkey 
import umysql
from datetime import datetime
monkey.patch_socket()

class Call(OutboundEventSocket):

    def __init__(self, socket, address, log, conn, conn_portab, filter=None):
        self.log = log
        self.conn = conn
        self.conn_portab = conn_portab

        self._action_queue = gevent.queue.Queue()

        OutboundEventSocket.__init__(self, socket, address, filter)


    def _protocol_send(self, command, args=""):
        self.log.info("[%s] args='%s'" % (command, args))
        response = super(Call, self)._protocol_send(command, args)
        self.log.info(str(response))
        return response

    def _protocol_sendmsg(self, name, args=None, uuid="", lock=False, loops=1):
        self.log.info("[%s] args=%s, uuid='%s', lock=%s, loops=%d" \
                      % (name, str(args), uuid, str(lock), loops))
        response = super(Call, self)._protocol_sendmsg(name, args, uuid, lock, loops)
        self.log.info(str(response))
        return response
  
    def on_channel_execute_complete(self, event):
        self.log.info("Event-Name: %s" % event.get_header('Event-Name') )
        self.log.info("Application: %s" % event.get_header('Application'))
        if event.get_header('Application') == 'bridge':
            self.hangup()

    def on_channel_hangup(self, event):
        self.log.info("Event-Name: %s" % event.get_header('Event-Name') )
        self.log.info(event)



    def run(self):
        self.connect()
        self.log.info("Channel Unique ID => %s" % self.get_channel_unique_id())

        self.env = {
            'destination': self._channel.get_header("Channel-Destination-Number"),
            'device_id': self._channel.get_header("variable_device_id"),
            'lcr': self._channel.get_header("variable_lcr"),
            'dialrule': self._channel.get_header("variable_dialrules"),
            'rategroup':  self._channel.get_header("variable_rategroup"),
            'destination_tags': '',
            'effective_caller_id_number': self._channel.get_header("effective_caller_id_number"),
            'effective_caller_id_name': self._channel.get_header("effective_caller_id_name"),
            'bypass_media': self._channel.get_header("bypass_media"),

            'accountcode_leg_a': self._channel.get_header("accountcode"),
            'customer_id': self._channel.get_header("variable_customer_id"),
            'device_name': self._channel.get_header("variable_device_name"),

            'user_rate_name': '',
            'user_rate_prefix': '',
            'user_rate_price': '',
            'user_rate_min_time': '',
            'user_rate_increment': '',
            'user_rate_tags': '',
            'user_rate_gracetime': '',

        }
        # only catch events for this channel

        
        self.myevents()
        self.set_bypass_media()
        #self.set_callerid()
        self.get_dialrules()
        self.get_carrier()
        if  self.get_userrates() and self.get_lcr():
            self.log.info("Completed")
            self.hangup()

        else:
            self.log.info("NOT Completed") 


    def set_bypass_media(self):
        if self.env['bypass_media'] == 'true':
            self.set("bypass_media=true")

    def set_callerid(self):
        self.set("effective_caller_id_number="+str(self.env['effective_caller_id_number']))
        self.set("effective_caller_id_name="+str(self.env['effective_caller_id_name']))

    def get_dialrules(self):
        ''' Get Dialrules in database '''
        self.log.info("> Getting dialrules")

        sql = '''SELECT CONCAT(dialrule.add,TRIM(LEADING dialrule.cut FROM '%(destination)s')), 
                dialrule.cut FROM ipsafe.dialrule WHERE dialrule_group_id='%(dialrule)s'
                AND (LENGTH('%(destination)s') BETWEEN dialrule.min_len AND dialrule.max_len) 
                AND LOCATE(dialrule.cut, '%(destination)s') = 1 ORDER BY LENGTH(dialrule.cut) 
                DESC LIMIT 1''' % self.env

        self.log.info("> Query: %s\n" % sql)

        res = None
        try:
            res = self.conn.fetchone(sql)
        except Exception, e:
            self.log.info("[-] Error = " + str(e))

        if res:
            self.log.info('> Destination number after dialrules: %s -> %s' % (self.env['destination'], res[0]))
            self.env['destination'] = res[0]

        else:
            self.log.info("> Dialrules not found in database\n")

    def get_carrier(self):
        self.set("commentary=")
        self.log.info('> Getting carrier and tags\n')

        def is_e164(number):
            if number[0:2] == '55' and len(number) > 11:
                return True
            else:
                return False

        if is_e164(self.env['destination']):
            number = self.env['destination'][2:]
        else:
            number = self.env['destination']

        #sql = '''select carrier, 'Movel' as tipo from portabilidade.portados where number = SUBSTRING('%s' FROM 3); ''' % number
        sql = '''select hold, 'Movel' as tipo from portabilidade.portados where number = '%s'; ''' % number

        res = None
        try:
            res = self.conn_portab.fetchone(sql)
        except Exception, e:
            self.log.info("[-] Error = " + str(e))

        self.log.info('> Query: %s\n' % sql)

        if not res:
            cn, prefix, mcdu = number[:2], number[2:len(number) - 4], number[-4:]

            sql = '''SELECT holding, tipo FROM portabilidade.anatel WHERE cn='%s'  AND pref='%s' 
            AND (mcdu_f >= '%s' AND mcdu_i <= '%s') LIMIT 1;''' % (cn, prefix, mcdu, mcdu)
            
            self.log.info('> Query: %s\n' % sql)

            res = self.conn_portab.fetchone(sql)
            if not res:
                #self.set("commentary=Not found in db portabilidade")
                self.set("commentary=Numero destino nao localizado na base de portabilidade")
                self.log.info('Not found in db portabilidade')
                self.env['destination_tags'] = ''

                return

        if res[1] == 'F':
            tipo = 'Fixo'
        else:
            tipo = 'Movel'
            #self.set("municipio=%s" % res[3])
            #self.set("area_local=%s" % res[4])
            #self.set("eot=%s" % res[2])

        self.env['destination_tags'] = '%s,%s' % (tipo, res[0])

        self.log.info('> Destination Tags: %s\n' % self.env['destination_tags'])


    def get_userrates(self):
        self.set( "hangup_commentary=")
        self.log.info('> Getting user rates\n')

        sql = '''SELECT rate_group.name, rate.increment, rate.min_time, rate.price, rate.prefix, rate.tags_string, rate_group.grace_time
                FROM rate_group INNER JOIN rate ON rate_group.id = rate.rate_group_id WHERE rate_group.id = '%(rategroup)s'
                AND (prefix = SUBSTRING('%(destination)s',1,length(prefix)) OR prefix = '*')
                ''' % (self.env)
        
        if(self.env['destination_tags'] != ''):
            sql += 'AND ('
            for tag in self.env['destination_tags'].split(','):
                sql += "tags_string LIKE '%" + tag + "%' OR "

            sql += "tags_string = '')"

        else:
            sql += " AND tags_string = ''"

        sql += ' ORDER BY price, length(prefix) DESC LIMIT 1'

        self.log.info('> Query: %s\n' % sql)

        rate = None
        try:
            rate = self.conn.fetchone(sql)
        except Exception, e:
            self.log.info("[-] Error = " + str(e))

        if rate:
            self.log.info('> RATES: Name (%s) / prefix (%s) / price (%s) / min_time (%s) / increment (%s) / tags (%s) \n' % (rate[0], rate[4], rate[3], rate[2], rate[1], rate[5]))
            
            #remover posteriormente
            self.set("user_rate_name=%s" % rate[0])
            self.set("user_rate_prefix=%s" % rate[4])
            self.set("user_rate_price=%s" % rate[3])
            self.set("user_rate_min_time=%s" % rate[2])
            self.set("user_rate_increment=%s" % rate[1])
            self.set("user_rate_tags=%s" % rate[5])
            self.set("user_rate_gracetime=%s" % rate[6])

            # manter
            self.env['user_rate_name'] = rate[0]
            self.env['user_rate_prefix'] = rate[4]
            self.env['user_rate_price'] = rate[3]
            self.env['user_rate_min_time'] = rate[2]
            self.env['user_rate_increment'] = rate[1]
            self.env['user_rate_tags'] = rate[5]
            self.env['user_rate_gracetime'] = rate[6]

            return True


        self.set( "hangup_commentary=Not found user rates to route")
        self.log.info('> Not found user rates to route\n')
        self.hangup(cause='404')
        return False

    def get_lcr(self):

        def _get_lcr_type():
            sql = '''SELECT lcr.order from lcr where id = %s''' % (self.env['lcr'])
            self.log.info('> Query: %s\n' % sql)

            try:
                res = self.conn.fetchone(sql)
            except Exception, e:
                self.log.info("[-] Error = " + str(e))
            else:
                self.set("lcr_order=%s" % res[0])         
                return res[0]

            return None

        self.log.info('> Search LCR\n')

        if(self.env['destination_tags'] != ''):
            where_clausule = 'AND ('
            for tag in self.env['destination_tags'].split(','):
                where_clausule += "tags_string LIKE '%" + tag + "%' OR "

            where_clausule += "tags_string = '')"

        else:
            where_clausule = " AND tags_string = ''"

        if _get_lcr_type() == 'price':
            where_clausule += ' ORDER BY price, length(prefix) DESC'
            where_clausule2 = ' ORDER BY c8, length(c9) DESC'
        
        else:
            where_clausule += ' ORDER BY priority, length(prefix) DESC'
            where_clausule2 = ' ORDER BY c13, length(c9) DESC'


        groupby_clausule = ') as tbl_rates GROUP BY c11'

        sql1 = '''(SELECT c0, c1, c2, c3, c4, c5, c6, c7,c8, c9, c10, c11, c12, c13, c14
                FROM ((SELECT DISTINCT lcr.name as c0,  provider.id as c1, gateway.name as c2, provider.name as c3,
                gateway.host as c4, rate_group.name as c5, rate.increment as c6, rate.min_time as c7,
                rate.price as c8, rate.prefix as c9, rate.tags_string as c10, gateway.id as c11, 
                gateway.description as c12, lcr_provider.priority as c13, rate_group.grace_time as c14
                FROM lcr 
                LEFT JOIN lcr_provider ON lcr_id = lcr.id 
                LEFT JOIN provider ON provider_id = provider.id 
                LEFT JOIN rate_group ON provider.rate_group_id = rate_group.id 
                LEFT JOIN rate ON rate_group.id = rate.rate_group_id 
                RIGHT JOIN gateway ON gateway.provider_id = provider.id 
                WHERE lcr.id = %(lcr)s AND lcr_provider.deactive = 0 
                AND rate.gateway_id AND rate.gateway_id = gateway.id
                AND (prefix = SUBSTRING('%(destination)s',1,length(prefix)) OR prefix = '*') 
                ''' % (self.env)
        sql1 +=  where_clausule + ')' + groupby_clausule + where_clausule2

        sql2 = '''(SELECT c0, c1, c2, c3, c4, c5, c6, c7,c8, c9, c10, c11, c12, c13, c14
                FROM ((SELECT DISTINCT lcr.name as c0,  provider.id as c1, gateway.name as c2, provider.name as c3,
                gateway.host as c4, rate_group.name as c5, rate.increment as c6, rate.min_time as c7,
                rate.price as c8, rate.prefix as c9, rate.tags_string as c10, gateway.id as c11, 
                gateway.description as c12, lcr_provider.priority as c13, rate_group.grace_time as c14
                FROM lcr
                LEFT JOIN lcr_provider ON lcr_id = lcr.id
                LEFT JOIN provider ON provider_id = provider.id
                LEFT JOIN rate_group ON provider.rate_group_id = rate_group.id
                LEFT JOIN rate ON rate_group.id = rate.rate_group_id
                RIGHT JOIN gateway ON gateway.provider_id = provider.id
                WHERE lcr.id = %(lcr)s AND lcr_provider.deactive = 0 
                AND gateway.id not in (select gateway.id from gateway inner join rate on gateway.id = rate.gateway_id)
                AND rate.gateway_id is NULL     
                AND (prefix = SUBSTRING('%(destination)s',1,length(prefix)) OR prefix = '*') 
                ''' % (self.env)
        sql2 +=  where_clausule + ')' + groupby_clausule + where_clausule2



        full_sql = sql1 + ' ) UNION ' + sql2 + ')' + where_clausule2
        self.log.info('> Query: %s\n' % full_sql)

        res = None
        try:
            res = self.conn.fetchall(full_sql)
        except Exception, e:
            self.log.info("[-] Error = " + str(e))

        if res:
            self.set("lcr_name=%s" % res[0][0])         
            dial_string = ""

            for counter, obj in enumerate(res):
                self.log.info('>LCR (%s)' % obj[0])
              
                sql2 = '''SELECT CONCAT(provider_rule.add,TRIM(LEADING provider_rule.cut FROM '%s')), 
                                provider_rule.cut FROM ipsafe.provider_rule WHERE provider_rule.gateway_id=%s
                                AND (LENGTH('%s') BETWEEN provider_rule.min_len AND provider_rule.max_len) 
                                AND LOCATE(provider_rule.cut, '%s') = 1 ORDER BY LENGTH(provider_rule.cut) 
                                DESC LIMIT 1''' % (self.env['destination'], obj[11], self.env['destination'], self.env['destination'])

                self.log.info('> Query: %s\n' % sql2)
             
                res2 = None
                try:
                    res2 = self.conn.fetchone(sql2)
                except Exception, e:
                    self.log.info("[-] Error = " + str(e))

                if res2:
                    self.log.info('> Destination number after Provider dialrules: %s -> %s' % (self.env['destination'], res2[0]))
                    new_destination = res2[0]
                else:
                    new_destination = self.env['destination']

                self.log.info(">>>> Calling provider: %s\n" % obj[3])
                self.log.info("--------------------------------\n")
                self.log.info(">>>>> Provider ID: %s\n" % obj[1])
                self.log.info(">>>>> Provider Name: %s\n" % obj[3])
                self.log.info(">>>>> Gateway Name: %s\n" % obj[2])
                self.log.info(">>>>> Host: %s\n" % obj[4])
                self.log.info(">>>>> Prefix: %s\n" % obj[9])
                self.log.info(">>>>> Rate: %s\n" % obj[8])
                self.log.info(">>>>> Tags: %s\n" % obj[10])
                self.log.info(">>>>> Destination: %s\n" % new_destination)

                # Gera dial string 

                dial_string += "["
                dial_string += "accountcode_leg_a=%s, " % self.env['accountcode']
                dial_string += "customer_id=%s, " % self.env['customer_id']
                dial_string += "device_id=%s, " % self.env['device_id']
                dial_string += "device_name=%s, " % self.env['device_name']
                dial_string += "lcr_name=%s, " % self.env['lcr']
                dial_string += "rategroup=%s, " % self.env['rategroup']
                dial_string += "user_rate_name=%s, " % self.env['user_rate_name']
                dial_string += "user_rate_prefix=%s, " % self.env['user_rate_prefix']
                dial_string += "user_rate_price=%s, " % self.env['user_rate_price']
                dial_string += "user_rate_min_time=%s, " % self.env['user_rate_min_time']
                dial_string += "user_rate_increment=%s, " % self.env['user_rate_increment']
                dial_string += "user_rate_tags=%s, " % self.env['user_rate_tags']
                dial_string += "user_rate_gracetime=%s, " % self.env['user_rate_gracetime']
                dial_string += "hangup_commentary=%s, " % self.env['hangup_commentary']
                dial_string += "commentary=%s, " % self.env['commentary']
                dial_string += "provider=%s, " % obj[1]
                dial_string += "provider_name=%s, " % obj[3]
                dial_string += "provider_gateway=%s, " % obj[11]
                dial_string += "provider_rate_name=%s, " % obj[5]
                dial_string += "provider_rate_prefix=%s, " % obj[9]
                dial_string += "provider_rate_price=%s, " % obj[8]
                dial_string += "provider_rate_min_time=%s, " % obj[7]
                dial_string += "provider_rate_increment=%s, " % obj[6]
                dial_string += "provider_rate_tags=%s," % obj[10]
                dial_string += "provider_rate_gracetime=%s" % obj[14]
                dial_string += "]"

                dial_string += "sofia/gateway/%s/%s|" % (obj[2], new_destination)

            self.log.info(">>>>> Dial String: %s\n" % dial_string)

            self.bridge(dial_string)
            return True

        else:
            self.set( "hangup_commentary=Not found provider rates to route")
            self.log.info('> Not found provider rates to route\n')
            self.hangup()
            return False


class Billing(OutboundServer):
    def __init__(self, address, handle_class, filter=None):
        self.log = FileLogger(logfile='/var/log/billing.log')
        #self.log = StdoutLogger()

        self.log.info("Start server %s ..." % str(address))

        self.conn = DBConnection()
        self.conn_portabilidade = DBConnection(host='186.226.87.8', database='portabilidade', limit=30)
        self.sim_calls = 0
        
        OutboundServer.__init__(self, address, handle_class, filter)

    def handle_request(self, socket, address):
        self.log.info("New request from %s" % str(address))
        self._requestClass(socket, address, self.log, self.conn, self.conn_portabilidade, self._filter)
        self.log.info("End request from %s" % str(address))


class DBConnection(object):
    def __init__(self, host='127.0.0.1', database='ipsafe', limit=100):
        self.log = StdoutLogger()
        self.maxsize = limit
        self.pool = Queue()
        self.size = 0
        self.host = host
        self.database = database
        self.port =  3306
        self.user = 'ipsafe' 
        self.password = 'config password'

    def get(self):
        self.log.info("[+] DBConnection.get")
        try:
            return self.pool.get_nowait()
        except:
            if self.size >= self.maxsize or self.pool.qsize():
                return self.pool.get()
            else:
                self.size += 1
                try:
                    new_item = umysql.Connection()
                    new_item.connect(self.host, self.port, self.user, self.password, self.database)
                except:
                    self.size -= 1
                    raise
                return new_item

    def put(self, item):
        self.log.info("[+] DBConnection.put")
        self.pool.put(item)  
       
    def closeall(self):
        while not self.pool.empty():
            conn = self.pool.get_nowait()
            try:
                conn.close()
            except Exception:
                pass 

    @contextlib.contextmanager
    def connection(self):
        self.log.info("[+] DBConnection.connection")
        conn = self.get()
        try:
            yield conn
        except:
            if not conn.is_connected():
                conn = None
                self.closeall()
            else:
                conn = self._rollback(conn)
            raise
        finally:
            if conn is not None and conn.is_connected():
                self.put(conn)

    @contextlib.contextmanager
    def query(self, *args, **kwargs):
        self.log.info("[+] DBConnection.query")
        with self.connection() as conn:
            try:
                yield conn.query(*args, **kwargs)
            except Exception, e:
                print("[-] Error = " + str(e))

    def _rollback(self, conn):
        try:
            conn.rollback()
        except:
            gevent.get_hub().handle_error(conn, *sys.exc_info())
            return
        return conn

    def execute(self, *args, **kwargs):
        self.log.info("[+] execute")
        with self.query(*args) as query:
            return len(query.rows)

    def fetchone(self, *args, **kwargs):
        self.log.info("[+] DBConnection.fetchone")
        with self.query(*args) as query:
            return query.rows[0]

    def fetchall(self, *args, **kwargs):
        with self.query(*args) as query:
            return query.rows



if __name__ == '__main__':

    billing = Billing(('127.0.0.1', 8084), Call)
    billing.serve_forever()
