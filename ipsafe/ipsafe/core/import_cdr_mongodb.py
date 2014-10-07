from pymongo.connection import Connection
from pymongo.errors import ConnectionFailure
import datetime
import sys
import pprint
import umysql
import math
import traceback

HANGUP_CAUSE = ['NORMAL_CLEARING', 'NORMAL_CLEARING', 'NORMAL_CLEARING',
                'NORMAL_CLEARING', 'USER_BUSY', 'NO_ANSWER', 'CALL_REJECTED',
                'INVALID_NUMBER_FORMAT']

# value 0 per default
# 1 in process of import, 2 imported successfully and verified
STATUS_SYNC = {"new": 0, "in_process": 1, "verified": 2}

def get_element_gw_tries(cdr):
    data_element = {}

    if 'uuid' in cdr['variables']:  
        data_element['uuid_b'] = cdr['variables']['uuid']
    else:
        data_element['uuid_b'] = ''

    if 'originating_leg_uuid' in cdr['variables']:  
        data_element['uuid_a'] = cdr['variables']['originating_leg_uuid']
    else:
        data_element['uuid_a'] = ''

    if 'provider_gateway' in cdr['variables']:  
        data_element['gateway_id'] = cdr['variables']['provider_gateway']
    else:
        data_element['gateway_id'] = None

    if 'provider_rate_name' in cdr['variables']:
        data_element['provider_rate_name'] = cdr['variables']['provider_rate_name']
    else:
        data_element['provider_rate_name'] = ''

    if 'provider_gateway' in cdr['variables']:  
        data_element['gateway_id'] = cdr['variables']['provider_gateway']
    else:
        data_element['gateway_id'] = None

    if 'start_stamp' in cdr['variables']:
        data_element['start_stamp'] = cdr['variables']['start_stamp']
    else:
        data_element['start_stamp'] = None

    if 'progress_media_stamp' in cdr['variables']:
        data_element['progressmedia_time'] = cdr['variables']['progress_media_stamp']
    else:
        data_element['progressmedia_time'] = 0

    if 'endpoint_disposition' in cdr['variables']:
        data_element['endpoint_disposition'] = cdr['variables']['endpoint_disposition']
    else:
        data_element['endpoint_disposition'] = ''

    if 'sip_hangup_disposition' in cdr['variables']:
        data_element['sip_hangup_disposition'] = cdr['variables']['sip_hangup_disposition']
    else:
        data_element['sip_hangup_disposition'] = ''    

    if 'hangup_cause' in cdr['variables']:
        data_element['hangup_cause'] = cdr['variables']['hangup_cause']
    else:
        data_element['hangup_cause'] = ''    

    if 'hangup_cause_q850' in cdr['variables']:
        data_element['hangup_cause_q850'] = cdr['variables']['hangup_cause_q850']
    else:
        data_element['hangup_cause_q850'] = ''    

    return data_element


def get_element(cdr, cdrb):
    """
    return some element from the cdr object
    """
    #Get accountcode
    if 'variables' in cdr and 'accountcode' in cdr['variables']:
        accountcode = cdr['variables']['accountcode']
    else:
        accountcode = ''
    #Get remote_media_ip
    if 'variables' in cdr and 'remote_media_ip' in cdr['variables']:
        remote_media_ip = cdr['variables']['remote_media_ip']
    else:
        remote_media_ip = ''
    #Get duration
    if cdrb:
        if 'variables' in cdrb and 'duration' in cdrb['variables'] \
           and cdrb['variables']['duration']:
            duration = float(cdrb['variables']['duration'])
        else:
            duration = 0

        if 'variables' in cdrb and 'billsec' in cdrb['variables'] \
            and cdrb['variables']['billsec']:
             billsec = cdrb['variables']['billsec']
        else:
            billsec = 0
    else:
        if 'variables' in cdr and 'duration' in cdr['variables'] \
           and cdr['variables']['duration']:
            duration = float(cdr['variables']['duration'])
        else:
            duration = 0
        #Get billsec
        billsec = 0
        
    #Get direction
    if 'variables' in cdr and 'direction' in cdr['variables']:
        direction = cdr['variables']['direction']
    else:
        direction = 'unknown'
    #Get uuid
    if 'variables' in cdr and 'uuid' in cdr['variables']:
        uuid = cdr['variables']['uuid']
    else:
        uuid = ''
    #Get caller_id_number
    if 'callflow' in cdr and 'caller_profile' in cdr['callflow'][0] \
       and 'caller_id_number' in cdr['callflow'][0]['caller_profile']:
        caller_id_number = cdr['callflow'][0]['caller_profile']['caller_id_number']
    else:
        caller_id_number = ''
    #Get caller_id_name
    if 'callflow' in cdr and 'caller_profile' in cdr['callflow'][0] \
       and 'caller_id_name' in cdr['callflow'][0]['caller_profile']:
        caller_id_name = cdr['callflow'][0]['caller_profile']['caller_id_name']
    else:
        caller_id_name = ''
    
    # Get read_codec
    if 'variables' in cdr and 'read_codec' in cdr['variables']:
        read_codec = cdr['variables']['read_codec']
    else:
        read_codec = ''
    # Get write_codec
    if 'variables' in cdr and 'write_codec' in cdr['variables']:
        write_codec = cdr['variables']['write_codec']
    else:
        write_codec = ''

    if 'variables' in cdr:
        if 'customer_id' in cdr['variables']:
            customer_id = cdr['variables']['customer_id']
        else:
            customer_id = 'null'

        if 'device_id' in cdr['variables']:
            device_id = cdr['variables']['device_id']
        else:
            device_id = ''

        if 'device_name' in cdr['variables']:
            device_name = cdr['variables']['device_name']
        else: 
            device_name = ''

        if 'lcr_name' in cdr['variables']:
            lcr_name = cdr['variables']['lcr_name']
        else:
            lcr_name = ''

        if 'rategroup' in cdr['variables']:
            rategroup = cdr['variables']['rategroup']
        else:
            rategroup = ''

        if 'start_stamp' in cdr['variables']:
            start_stamp = cdr['variables']['start_stamp']
        else:
            start_stamp = 0

        if 'end_stamp' in cdr['variables']:
            end_stamp = cdr['variables']['end_stamp']
        else:
            end_stamp = 0

        if 'hangup_cause' in cdr['variables']:
            hangup_cause = cdr['variables']['hangup_cause']
        else:
            hangup_cause = ''

        if 'endpoint_disposition' in cdr['variables']:
            endpoint_disposition = cdr['variables']['endpoint_disposition']
        else:
            endpoint_disposition = ''

        if 'sip_hangup_disposition' in cdr['variables']:
            sip_hangup_disposition = cdr['variables']['sip_hangup_disposition']
        else:
            sip_hangup_disposition = ''

        if 'user_rate_name' in cdr['variables']:
            user_rate_name = cdr['variables']['user_rate_name']
        else:
            user_rate_name = ''

        if 'user_rate_prefix' in cdr['variables']:
            user_rate_prefix = cdr['variables']['user_rate_prefix']
        else:
            user_rate_prefix = ''            

        if 'user_rate_price' in cdr['variables']:
            user_rate_price = cdr['variables']['user_rate_price']
        else:
            user_rate_price = 0

        if 'user_rate_min_time' in cdr['variables']:
            user_rate_min_time = cdr['variables']['user_rate_min_time']
        else:
            user_rate_min_time = 0

        if 'user_rate_increment' in cdr['variables']:
            user_rate_increment = cdr['variables']['user_rate_increment']
        else:
            user_rate_increment = 0

        if 'user_rate_tags' in cdr['variables']:
            user_rate_tags = cdr['variables']['user_rate_tags']
        else:
            user_rate_tags = ''

        if 'user_rate_gracetime' in cdr['variables']:
            user_rate_gracetime = cdr['variables']['user_rate_gracetime']

        else:
            user_rate_gracetime = 0

        if 'progress_media_stamp' in cdr['variables']:
            progressmedia_time = cdr['variables']['progress_media_stamp']
        else:
            progressmedia_time = 0

        if 'sip_received_ip' in cdr['variables']:
            sip_received_ip = cdr['variables']['sip_received_ip']
        else:
            progressmedia_time = 0

        if 'hangup_commentary' in cdr['variables']:
            hangup_commentary = cdr['variables']['hangup_commentary']
        else:
            hangup_commentary = ''
       
        if 'commentary' in cdr['variables']:
            commentary = cdr['variables']['commentary']
        else:
            commentary = ''
       
        if 'sip_via_host' in cdr['variables']:
            sip_via_host = cdr['variables']['sip_via_host']
        else:
            sip_via_host = ''       

        if 'sip_to_port' in cdr['variables']:
            sip_to_port = cdr['variables']['sip_to_port']
        else:
            sip_to_port = ''
       
        if 'sip_user_agent' in cdr['variables']:
            sip_user_agent = cdr['variables']['sip_user_agent']
        else:
            sip_user_agent = ''
       
        if 'sip_contact_uri' in cdr['variables']:
            sip_contact_uri = cdr['variables']['sip_contact_uri']
        else:
            sip_contact_uri = ''
       
       
    if  cdrb and 'variables' in cdrb:
        
        if 'provider_rate_name' in cdrb['variables']:
            provider_rate_name = cdrb['variables']['provider_rate_name']
        else:
            provider_rate_name = ''

        if 'provider_rate_prefix' in cdrb['variables']:
            provider_rate_prefix = cdrb['variables']['provider_rate_prefix']
        else:
            provider_rate_prefix = ''

        if 'provider_rate_price' in cdrb['variables']:
            provider_rate_price = cdrb['variables']['provider_rate_price']
        else:
            provider_rate_price = 0

        if 'provider_rate_min_time' in cdrb['variables']:
            provider_rate_min_time = cdrb['variables']['provider_rate_min_time']
        else:
            provider_rate_min_time = 0

        if 'provider_rate_increment' in cdrb['variables']:
            provider_rate_increment = cdrb['variables']['provider_rate_increment']
        else:
            provider_rate_increment = 0

        if 'provider_rate_tags' in cdrb['variables']:
            provider_rate_tags = cdrb['variables']['provider_rate_tags']

        else:
            provider_rate_tags = ''

        if 'provider_rate_gracetime' in cdrb['variables']:
            provider_rate_gracetime = cdrb['variables']['provider_rate_gracetime']

        else:
            provider_rate_gracetime = 0

        if 'provider' in cdrb['variables']:  
            provider_id = cdrb['variables']['provider']
        else:
            provider_id = 'NULL'

        if 'provider_gateway' in cdrb['variables']:  
            gateway_id = cdrb['variables']['provider_gateway']
        else:
            gateway_id = 'NULL'

        if 'progress_mediasec' in cdrb['variables']:
            progress_mediasec = cdrb['variables']['progress_mediasec']
        else:
            progress_mediasec = 0

        if 'uuid' in cdrb['variables']:
            uuid_b = cdrb['variables']['uuid']
        else:
            uuid_b = ''
    else:

        provider_rate_name = ''
        provider_rate_prefix = ''
        provider_rate_price = 0
        provider_rate_min_time = 0
        provider_rate_increment = 0
        provider_rate_tags = ''
        provider_rate_gracetime = 0
        provider_id = 'NULL'
        gateway_id = 'NULL'
        progress_mediasec = 0
        uuid_b = ''


    data_element = {
        'accountcode': accountcode,
        'remote_media_ip': remote_media_ip,
        'caller_id_number': caller_id_number,
        'caller_id_name': caller_id_name,
        'duration': duration,
        'billsec': billsec,
        'direction': direction,
        'uuid': uuid,
        'uuid_b': uuid_b,
        'read_codec': read_codec,
        'write_codec': write_codec,
        'customer_id': customer_id,
        'device_id': device_id,
        'device_name': device_name,
        'lcr_name': lcr_name,
        'rategroup': rategroup,
        'start_stamp': start_stamp,
        'end_stamp': end_stamp,
        'provider_id': provider_id,
        'gateway_id': gateway_id,

        'hangup_cause': hangup_cause,
        'endpoint_disposition': endpoint_disposition,
        'sip_hangup_disposition': sip_hangup_disposition,
        'provider_rate_name': provider_rate_name,
        'provider_rate_prefix': provider_rate_prefix,
        'provider_rate_price': provider_rate_price,
        'provider_rate_min_time': provider_rate_min_time,
        'provider_rate_increment': provider_rate_increment,
        'provider_rate_tags': provider_rate_tags,
        'provider_rate_gracetime': provider_rate_gracetime,
        'user_rate_name': user_rate_name,
        'user_rate_prefix': user_rate_prefix,
        'user_rate_price': user_rate_price,
        'user_rate_min_time': user_rate_min_time,
        'user_rate_increment': user_rate_increment,
        'user_rate_tags': user_rate_tags,
        'user_rate_gracetime': user_rate_gracetime,
        'progress_mediasec': progress_mediasec,
        'sip_received_ip': sip_received_ip,
        'hangup_commentary': hangup_commentary,
        'commentary': commentary,
        'sip_via_host': sip_via_host,
        'sip_to_port': sip_to_port,
        'sip_user_agent': sip_user_agent,
        'sip_contact_uri': sip_contact_uri,
    }

    return data_element

def func_importcdr_aggregate(importcdr_handler, cdr_handler_processed):
    """
    function go through the current mongodb, then will
    - create CDR_COMMON
    - build the pre-aggregate
    """

    def _get_user_billsec(data):
        if int(data['billsec']) > int(data['user_rate_gracetime']):
            if data['billsec'] < data['user_rate_min_time']:
                user_billsec = data['user_rate_min_time']
            else:
                user_billsec = math.ceil(float(data['billsec']) / float(data['user_rate_increment'])) * float(data['user_rate_increment'])
        else:
            user_billsec = 0

        return int(user_billsec)

    def _get_provider_billsec(data):
        if int(data['billsec']) > int(data['provider_rate_gracetime']):
            if data['billsec'] < data['provider_rate_min_time']:
                provider_billsec = data['provider_rate_min_time']
            else:
                provider_billsec = math.ceil(float(data['billsec']) / float(data['provider_rate_increment'])) * float(data['provider_rate_increment'])
        else:
            provider_billsec = 0
        return int(provider_billsec)

    def _get_user_cost(data, user_billsec):
        return user_billsec * float(data['user_rate_price']) / 60
    
    def _get_provider_cost(data, provider_billsec):
        return provider_billsec * float(data['provider_rate_price']) / 60
      

    #We limit the import tasks to a maximum - 1000
    #This will reduce the speed but that s the only way to make sure
    #we dont have several time the same tasks running

    PAGE_SIZE = 1000
    count_import = 0
    count_error = 0
    #Store cdr in list to insert by bulk
#    cdr_bulk_record = []

    result = importcdr_handler.find(
        {
            'channel_data.direction': 'inbound',
            '$or': [{'import_cdr': {'$exists': False}},
                {'import_cdr': 0}]
        }
        ).limit(PAGE_SIZE)

    #Retrieve FreeSWITCH CDRs

 #   for cdr in result:
 #       print '-'*60
 #       pprint.pprint(cdr)

 #   return

    mariadb = umysql.Connection()
    mariadb.connect('127.0.0.1', 3306, 'ipsafe', 'password', 'ipsafe')

    for cdr in result:
        #print '-'*80
        print 'Processing CDR'
        #pprint.pprint(cdr)

        # Check Destination number
        destination_number = cdr['callflow'][0]['caller_profile']['destination_number']
        hangup_cause_q850 = cdr['variables']['hangup_cause_q850']

        if 'bridge_uuid' in cdr['variables']:
            cdr_legb_uuid = cdr['variables']['bridge_uuid']

        elif 'origination' in cdr['callflow'][0]['caller_profile'] and 'uuid' in cdr['callflow'][0]['caller_profile']['origination']:
            cdr_legb_uuid = cdr['callflow'][0]['caller_profile']['origination']['uuid']

        else:
            cdr_legb_uuid = None

        if cdr_legb_uuid:
            cdr_b = importcdr_handler.find(
            {
                'callflow.caller_profile.uuid': cdr_legb_uuid
            })[0]
        else:
            cdr_b = None

        #Retrieve Element from CDR Object
        #pprint.pprint(cdr_b[0])

        data_element = get_element(cdr, cdr_b)

        if cdr_b:
            print 'Found B leg'
            user_billsec = _get_user_billsec(data_element)
            provider_billsec = _get_provider_billsec(data_element)
            user_cost = _get_user_cost(data_element, user_billsec)
            provider_cost = _get_provider_cost(data_element, provider_billsec)
            print 'User billsec: %s - Provider billsec: %s' % (str(user_billsec), str(provider_billsec))
        else:
            print 'Not found B leg'
            user_billsec = 0
            provider_billsec = 0
            user_cost = 0
            provider_cost = 0

        cdr_record = {
            'customer': data_element['customer_id'],
            'uuid': data_element['uuid'],
            'uuid_b': data_element['uuid_b'],
            'accountcode': data_element['accountcode'],
            'caller_id_number': data_element['caller_id_number'],
            'caller_id_name': data_element['caller_id_name'],
            'device_id': data_element['device_id'],
            'destination_number': destination_number,
            'lcr_name': data_element['lcr_name'],
            'rate_group': data_element['rategroup'],
            'start_time': data_element['start_stamp'],
            'end_time': data_element['end_stamp'],
            'billsec': data_element['billsec'],
            'duration': data_element['duration'],
            'provider': data_element['provider_id'], 
            'gateway': data_element['gateway_id'],    
            'hangup_cause': data_element['hangup_cause'],
            'hangup_cause_q850': hangup_cause_q850,
            'remote_media_ip': data_element['remote_media_ip'],
            'endpoint_disposition': data_element['endpoint_disposition'],
            'hangup_disposition': data_element['sip_hangup_disposition'],
            'read_codec': data_element['read_codec'],
            'write_codec': data_element['write_codec'],
            'cdr_object_id': cdr['_id'],
            'user_billsec': user_billsec,
            'provider_billsec': provider_billsec,
            'provider_cost': provider_cost,
            'user_cost': user_cost,
            'provider_rate_name': data_element['provider_rate_name'],
            'provider_rate_prefix': data_element['provider_rate_prefix'],
            'provider_rate_price':  data_element['provider_rate_price'],
            'provider_rate_min_time': data_element['provider_rate_min_time'],
            'provider_rate_increment': data_element['provider_rate_increment'],
            'provider_rate_tags': data_element['provider_rate_tags'],
            'provider_rate_gracetime': data_element['provider_rate_gracetime'],
            'user_rate_name': data_element['user_rate_name'],
            'user_rate_prefix': data_element['user_rate_prefix'],
            'user_rate_price':  data_element['user_rate_price'],
            'user_rate_min_time': data_element['user_rate_min_time'],
            'user_rate_increment': data_element['user_rate_increment'],
            'user_rate_tags': data_element['user_rate_tags'],
            'user_rate_gracetime': data_element['user_rate_gracetime'],
            'progressmedia_time': data_element['progress_mediasec'],
            'sip_received_ip': data_element['sip_received_ip'],
            'hangup_commentary': data_element['hangup_commentary'],
            'commentary': data_element['commentary'],
            'sip_via_host': data_element['sip_via_host'],
            'sip_to_port': data_element['sip_to_port'],
            'sip_user_agent': data_element['sip_user_agent'],
            'sip_contact_uri': data_element['sip_contact_uri'],
        }

        #pprint.pprint(cdr_record)


        # Append cdr to bulk_cdr list
 #       cdr_bulk_record.append(cdr_record)

        # Count CDR import
 #       local_count_import = local_count_import + 1

        sql = '''
                INSERT INTO ipsafe.cdr 
                    (customer_id, uuid, uuid_b, accountcode, caller_id, device_id, destination_number, lcr_name, rate_group, start_time, end_time, billsec, duration, provider_id,
                    gateway_id, hangup_cause, hangup_cause_q850, remote_media_ip, endpoint_disposition, hangup_disposition, read_codec, write_codec, cdr_object_id, user_billsec,
                    provider_billsec, provider_cost, user_cost, provider_rate_name, provider_rate_prefix, provider_rate_price, provider_rate_min_time, provider_rate_increment,
                    provider_rate_tags, user_rate_name, user_rate_prefix, user_rate_price, user_rate_min_time, user_rate_increment, user_rate_tags, progressmedia_time, user_rate_gracetime, provider_rate_gracetime, sip_received_ip,
                    hangup_commentary, commentary, sip_via_host, sip_to_port, sip_user_agent, sip_contact_uri) 
                VALUES 
                    ('%(customer)s', '%(uuid)s','%(uuid_b)s','%(accountcode)s','%(caller_id_name)s <%(caller_id_number)s>','%(device_id)s','%(destination_number)s','%(lcr_name)s','%(rate_group)s',
                     '%(start_time)s','%(end_time)s','%(billsec)s', '%(duration)s', %(provider)s, %(gateway)s, '%(hangup_cause)s', '%(hangup_cause_q850)s', '%(remote_media_ip)s','%(endpoint_disposition)s',
                     '%(hangup_disposition)s', '%(read_codec)s', '%(write_codec)s','%(cdr_object_id)s','%(user_billsec)s', '%(provider_billsec)s', '%(provider_cost)s','%(user_cost)s','%(provider_rate_name)s',
                     '%(provider_rate_prefix)s', '%(provider_rate_price)s','%(provider_rate_min_time)s','%(provider_rate_increment)s', '%(provider_rate_tags)s', '%(user_rate_name)s', '%(user_rate_prefix)s',
                     '%(user_rate_price)s','%(user_rate_min_time)s','%(user_rate_increment)s', '%(user_rate_tags)s', '%(progressmedia_time)s', '%(user_rate_gracetime)s', '%(provider_rate_gracetime)s', '%(sip_received_ip)s',
                     '%(hangup_commentary)s', '%(commentary)s', '%(sip_via_host)s', '%(sip_to_port)s', '%(sip_user_agent)s', '%(sip_contact_uri)s')
                ''' % cdr_record
                     
        
        try:
            if (cdr_record['customer'] == 'null' and cdr_record['duration'] == 0):
                print 'Delting record: %s - because customer is null and duration is 0' % cdr['_id']
                importcdr_handler.remove( {'_id': cdr['_id']}, )
                
            else:
                print 'SQL: %s' % sql
                result = mariadb.query(sql)
                print result            

        except umysql.SQLError, e:
            print 'Error: %s' % e
            count_error = count_error + 1
   
        else:
        # Flag the CDR as imported
            
            importcdr_handler.update(
                {'_id': cdr['_id']},
                {
                    '$set': {
                        'import_cdr': 1,
                    }
                }
            )
            ''' 
            if cdr_b:
                importcdr_handler.update(
                    {'_id': cdr_b['_id']},
                    {
                        '$set': {
                            'import_cdr': 1,
                        }
                    }
                )
            '''
            count_import = count_import + 1



        # Get list of tries (gateways)
        #gw_tries = importcdr_handler.find({'variables.originating_leg_uuid': cdr_record['uuid']})
        gw_tries = importcdr_handler.find({
                'channel_data.direction': 'outbound',
                'variables.originating_leg_uuid': cdr_record['uuid'],
                'import_cdr': {'$exists': False},
            })

        for cdr in gw_tries:
            data_element = get_element_gw_tries(cdr)
            print 'Importing gw try'
            pprint.pprint(data_element)
            sql = '''
                    INSERT INTO ipsafe.cdr_tries 
                        (uuid_a, uuid_b, start_time, gateway_id, hangup_cause, hangup_cause_q850, endpoint_disposition, hangup_disposition, provider_rate_name, 
                            progressmedia_time) 
                    VALUES 
                        ('%(uuid_a)s','%(uuid_b)s','%(start_stamp)s',%(gateway_id)s, '%(hangup_cause)s', '%(hangup_cause_q850)s', '%(endpoint_disposition)s',
                         '%(sip_hangup_disposition)s', '%(provider_rate_name)s', '%(progressmedia_time)s') 
                    ''' % data_element
                         

            print 'SQL: %s' % sql
            try:
                result = mariadb.query(sql)
                print result            

            except umysql.SQLError, e:
                print 'Error: %s' % e
                count_error = count_error + 1
       
            else:
            # Flag the CDR as imported
                importcdr_handler.update(
                    {'_id': cdr['_id']},
                    {
                        '$set': {
                            'import_cdr': 1,
                        }
                    }
                )



    tagged = importcdr_handler.find({'import_cdr': {'$exists': True},})
    for cdr in tagged:
        print 'moving and deleting cdr record for: %s' % cdr['_id']
        try:
            cdr_handler_processed.insert(cdr)
            importcdr_handler.remove({'_id': cdr['_id'],})
        except Exception, e:
            traceback.print_exc()


    print("Total Record(s) imported:%d" %
        (count_import))
    print("Total Record(s) ERROR:%d" %
        (count_error))

def import_cdr_freeswitch_mongodb():
    # Browse settings.CDR_BACKEND and for each IP check if the IP exist
    # in our Switch objects. If it does we will connect to that Database
    # and import the data as we do below

    print("Starting the synchronization...")


    #Connect to Database
    db_name = 'ipsafe'
    table_name = 'cdr'
    table_name_processed_cdr = 'processed_cdr'
    host = '127.0.0.1'
    port = 27017

    #Connect on MongoDB Database
    try:
        connection = Connection(host, port)
        connection_processed = Connection(host, port)
        DBCON = connection[db_name]
        DBCON_PROCESSED = connection_processed[db_name]
    except ConnectionFailure, e:
        sys.stderr.write("Could not connect to MongoDB: %s - %s" %
            (e, ipaddress))
        sys.exit(1)

    #Connect to Mongo
    cdr_handler = DBCON[table_name]
    cdr_handler_processed = DBCON_PROCESSED[table_name_processed_cdr]
    #Start import for this mongoDB
    func_importcdr_aggregate(cdr_handler, cdr_handler_processed)

if __name__ == '__main__':
    try:
        import_cdr_freeswitch_mongodb()
    except:
        raise
