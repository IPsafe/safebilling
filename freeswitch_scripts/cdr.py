# -*- coding: utf-8 -*-

from plivo.core.errors import ConnectError
from plivo.utils.logger import StdoutLogger
from datetime import datetime
from plivo.core.freeswitch.inboundsocket import InboundEventSocket

import pprint
import gevent
import traceback

class CDR(InboundEventSocket):
    def __init__(self, host, port, password, filter="ALL", log=None, cdr_conn=None):
        InboundEventSocket.__init__(self, host, port, password, filter)
        self.log = log
        self.conn = cdr_conn

    def create_cdr(self, ev):
        def _get_user_billsec(self):
            if self.cdr['billsec'] > 0:
                if self.cdr['billsec'] < self.cdr['user_rate_min_time']:
                    user_billsec = self.cdr['user_rate_min_time']
                else:
                    user_billsec = math.ceil(float(self.cdr['billsec']) / float(self.cdr['user_rate_increment'])) * self.cdr['user_rate_increment']
            else:
                user_billsec = 0

            return int(user_billsec)

        def _get_provider_billsec(self):
            if int(self.cdr['billsec']) > 0:
                if self.cdr['billsec'] < self.cdr['provider_rate_min_time']:
                    provider_billsec = self.cdr['provider_rate_min_time']
                else:
                    provider_billsec = math.ceil(float(self.cdr['billsec']) / float(self.cdr['provider_rate_increment'])) * self.cdr['provider_rate_increment']
            else:
                provider_billsec = 0
            return int(provider_billsec)

        def _get_user_cost(self):
            try:
                cost = self.cdr['user_billsec'] * float(self.cdr['user_rate_price']) / 60
            except TypeError:
                print repr(self.cdr['provider_rate_price'])
                raise

            return cost
        def _get_provider_cost(self):
            try:
                cost = self.cdr['provider_billsec'] * float(self.cdr['provider_rate_price']) / 60
            except TypeError:
                print repr(self.cdr['provider_rate_price'])
                raise

            return cost

        try:
            self.cdr = {
                    'customer': ev.get_header("variable_customer_id"),
                    'device_id': ev.get_header("variable_device_id"),
                    'caller_id_name': ev.get_header("Caller-Caller-ID-Name"),
                    'caller_id_number': ev.get_header("Caller-Caller-ID-Number"),
                    'destination_number': ev.get_header("Caller-Destination-Number"),
                    #'bridged_time': datetime.fromtimestamp(float(ev.get_header("Caller-Channel-Bridged-Time")[:10])).strftime('%Y-%m-%d %H:%M:%S'),
                    'created_time': datetime.fromtimestamp(float(ev.get_header("Caller-Channel-Created-Time")[:10])).strftime('%Y-%m-%d %H:%M:%S'),
                    'answered_time': datetime.fromtimestamp(float(ev.get_header("Caller-Channel-Answered-Time")[:10])).strftime('%Y-%m-%d %H:%M:%S'),
                    'hangup_time': datetime.fromtimestamp(float(ev.get_header("Caller-Channel-Hangup-Time")[:10])).strftime('%Y-%m-%d %H:%M:%S'),
                    'hangup_cause': ev.get_header("variable_hangup_cause"),
                    
                    'billsec': ev.get_header("variable_billsec"),
                    'duration': ev.get_header("variable_duration"),
                    'context': ev.get_header("Caller-Context"),
                    'uri': ev.get_header("variable_sip_to_uri"),
                    #'start_uepoch': ev.get_header("variable_start_uepoch"),
                    #'end_uepoch': ev.get_header("variable_end_uepoch"),
                    'received_ip': ev.get_header("variable_sip_received_ip"),
                    'answer_ms': ev.get_header("variable_answermsec"),
                    'last_arg': ev.get_header("variable_last_arg"),
                    'hangup_disposition': ev.get_header("variable_sip_hangup_disposition"),
                    'endpoint_disposition': ev.get_header("variable_endpoint_disposition"),
                    'answer_stamp': ev.get_header("variable_answer_stamp"),
                    'start_stamp': ev.get_header("variable_start_stamp"),
                    'end_stamp': ev.get_header("variable_end_stamp"),
                    'progress_media_stamp': ev.get_header("variable_progress_media_stamp"),

                    'uuid':  ev.get_header("Unique-ID"),
                    'uuid_b': ev.get_header("Other-Leg-Unique-ID"),
                    'provider_name': ev.get_header("variable_provider_name"),
                    'provider_total':  ev.get_header("variable_rategroup"),
                    'user_total':  ev.get_header("variable_rategroup"),
                    'call_direction':  ev.get_header("Call-Direction"),
                    'accountcode':  ev.get_header("variable_accountcode"),
                    'device_id':  ev.get_header("variable_device_id"),
                    'lcr_name':  ev.get_header("variable_lcr_name"),

                    'read_codec': ev.get_header("Channel-Read-Codec-Name"),
                    'write_codec': ev.get_header("Channel-Write-Codec-Name"),

                    'user_rate_name':  ev.get_header("variable_user_rate_name"),
                    'user_rate_prefix': ev.get_header("variable_user_rate_prefix"),
                    'user_rate_price': ev.get_header("variable_user_rate_price"),
                    'user_rate_min_time': ev.get_header("variable_user_rate_min_time"),
                    'user_rate_increment': ev.get_header("variable_user_rate_increment"),
                    'user_rate_tags': ev.get_header("variable_user_rate_tags"),
                   

                    'provider_rate_name':  ev.get_header("variable_provider_rate_name"),
                    'provider_rate_prefix': ev.get_header("variable_provider_rate_prefix"),
                    'provider_rate_price': ev.get_header("variable_provider_rate_price"),
                    'provider_rate_min_time': ev.get_header("variable_provider_rate_min_time"),
                    'provider_rate_increment': ev.get_header("variable_provider_rate_increment"),
                    'provider_rate_tags': ev.get_header("variable_provider_rate_tags"),
                }


            self.cdr['user_billsec'] = _get_user_billsec(self)
            self.cdr['provider_billsec'] = _get_provider_billsec(self)
            self.cdr['user_cost'] = _get_user_cost(self)
            self.cdr['provider_cost'] = _get_provider_cost(self)

            print 'debug cdr'
            pprint.pprint(self.cdr)
            
            #if (self.cdr['call_direction'] == 'inbound'):
            #    sql = '''
            #        UPDATE ipsafe.cdr 
            #            SET 
            #
            #            lcr_name = '%s'
            #
            #        WHERE uuid = '%s'
            #        ''' % (                            
            #                self.cdr['lcr_name'], self.cdr['uuid'],
            #             )
            #
            #    print 'SQL: %s' % sql
            #    self.conn.execute(sql)
            

            if (self.cdr['call_direction'] == 'outbound'):
                sql = '''
                    UPDATE ipsafe.cdr 
                        SET start_time = '%s',
                        end_time = '%s',
                        provider_total = '%s', 
                        provider_name = '%s', 
                        user_total = '%s',
                        billsec = '%s', 
                        duration = '%s',
                        hangup_cause = '%s',
                        endpoint_disposition = '%s',
                        hangup_disposition = '%s'
                    WHERE uuid = '%s'
                    ''' % (                            
                            self.cdr['start_stamp'], self.cdr['end_stamp'], self.cdr['provider_total'], self.cdr['provider_name'], self.cdr['user_total'], 
                            self.cdr['billsec'], self.cdr['duration'], self.cdr['hangup_cause'], self.cdr['endpoint_disposition'], self.cdr['hangup_disposition'],
                            self.cdr['uuid_b'],
                         )

                print 'SQL: %s' % sql
                self.conn.execute(sql)
    
        except Exception,e:
            traceback.print_exc()


    def on_channel_create(self, ev):
        self.log.info("Event-Name: %s" % ev.get_header('Event-Name') )
        try:
            
            self.create = {
                'uuid': ev.get_header("Unique-ID"),
                'customer': ev.get_header("variable_customer_id"),
                'device_id': ev.get_header("variable_device_id"),
                'device_name': ev.get_header("variable_device_name"),
                'accountcode':  ev.get_header("variable_accountcode"),
                'caller_id_name': ev.get_header("Caller-Caller-ID-Name"),
                'caller_id_number': ev.get_header("Caller-Caller-ID-Number"),
                'caller_ip': ev.get_header("Caller-Caller-ID-Number"),
                'destination_number': ev.get_header("Caller-Destination-Number"),

                'provider_name':  ev.get_header("variable_provider_name"),
                'lcr_name':  ev.get_header("variable_lcr_name"),
                'rate_group':  ev.get_header("variable_rategroup"),

                'created_time': datetime.fromtimestamp(float(ev.get_header("Caller-Channel-Created-Time")[:10])).strftime('%Y-%m-%d %H:%M:%S'),
                'call_direction':  ev.get_header("Call-Direction"),
            }

            print 'channel create'
            

            if (self.create['call_direction'] == 'inbound'):
                sql = '''
                    INSERT INTO ipsafe.cdr 
                        (customer, caller_id, device_id, device_name, accountcode, lcr_name, rate_group, destination_number, start_time, uuid, provider_name) 
                    VALUES 
                        ('%s','%s <%s>','%s','%s','%s','%s','%s','%s','%s', '%s', '%s') 
                    ''' % (
                            self.create['customer'], self.create['caller_id_name'], self.create['caller_id_number'], self.create['device_id'], self.create['device_name'], 
                            self.create['accountcode'], self.create['lcr_name'], self.create['rate_group'], self.create['destination_number'], self.create['created_time'], 
                            self.create['uuid'], self.create['provider_name'],
                         )

                print 'SQL: %s' % sql
                self.conn.execute(sql)
                pprint.pprint(self.create)


        except Exception,e:
            traceback.print_exc()

    def on_channel_hangup(self, ev):
        '''
        Receives callbacks for BACKGROUND_JOB ev.
        '''
        #self.log.info("Event-Name: %s" % ev.get_header('Event-Name') )
        #self.log.debug('on_channel_hangup: %s' % ev)

    def on_channel_hangup_complete(self, ev):
        self.log.info("Event-Name: %s" % ev.get_header('Event-Name') )
        #self.log.debug('on_channel_hangup: %s' % ev)
        self.create_cdr(ev)


def dispatch_requests(env, start_response):
    start_response('404 Not Found', [('Content-Type', 'text/html')])
    return ['<h1>Wrong Usage - Command Not found</h1>']
