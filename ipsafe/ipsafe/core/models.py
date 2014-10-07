# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.generic import GenericRelation
from django.db.models import Sum

import re

class Customer(models.Model):
    name = models.CharField(max_length=80, verbose_name='Nome')
    email = models.CharField(max_length=80, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    web_site = models.URLField(u'Site', blank=True)
    address =  models.TextField(u'Endereço', blank=True)
    devices_limit = models.IntegerField(null=True,blank=True)
    max_calls = models.IntegerField(null=True,blank=True, verbose_name='Limite de chamadas ativas')
    calls_per_second = models.PositiveIntegerField('Chamadas por segundo', default=10, help_text="Máximo de chamadas por segundo", null=True, blank=True)
    customer_balance = models.DecimalField(u'Balanço', max_digits=12, decimal_places=6, default=0.0,  help_text=u"Balanço atual do cliente.")
    postpaid_limit = models.DecimalField(null=True,blank=True, max_digits=8, decimal_places=2, verbose_name='Limite Pos-Pago')
    lcr = models.ForeignKey('Lcr', verbose_name='LCR')
    rate_groups = models.ForeignKey('RateGroup',verbose_name='Tarifas')
    user = models.ForeignKey(User, unique=True, verbose_name=u'Usuário', null=True, blank=True)

    class Meta:
        db_table = 'customer'
        verbose_name = u"Cliente"
        verbose_name_plural = u"Clientes"
    def __unicode__(self):
        return self.name


class Blacklist(models.Model):
    did = models.CharField(u'Número', max_length=30, blank=False, null=False)
    description = models.CharField(u'Descrição', max_length=255, blank=False, null=False)
    class Meta:
        db_table = 'blacklist'
        verbose_name = u"Blacklist"
        verbose_name_plural = u"Blacklist"
    def __unicode__(self):
        return self.did
    
class Codec(models.Model):
    codec = models.CharField(max_length=10)
    class Meta:
        db_table = 'codec'
        verbose_name = u"Codec"
        verbose_name_plural = u"Codecs"
    def __unicode__(self):
        return self.codec

class Device(models.Model):
    customer = models.ForeignKey('Customer', null=False, blank=False,verbose_name='Cliente')
    dialrules_groups = models.ForeignKey('DialruleGroup', null=True, blank=True,verbose_name='Regras de Discagem')
    name = models.CharField('Device',max_length=80,unique=True,blank=False,null=False)
    description = models.CharField(u'Descrição',max_length=80,null=False,blank=True)
    device_type = models.CharField(max_length=20, blank=True,default='extension')
    accountcode = models.CharField(max_length=20, null=True, blank=True)
    callerid = models.CharField(u'CallerID (Nome)',max_length=80, null=True, blank=True)
    callerid_number = models.CharField(u'CallerID (Número)',max_length=80, null=True, blank=True)
    context = models.CharField(max_length=80, null=True,blank=True,default='default')
    host = models.CharField(max_length=31, blank=True, null=True)
    port = models.CharField('Porta',max_length=5, null=True,blank=True,default='5060')
    password = models.CharField('Senha',max_length=80, blank=True, null=True)
    codec_inbound = models.CharField(max_length=80, null=True,verbose_name='Codec Inbound')
    codec_outbound = models.CharField(max_length=80, null=True,verbose_name='Codec Outbound')
    codec_inbound_string = models.CharField(max_length=200, null=True)
    codec_outbound_string = models.CharField(max_length=200, null=True)
    bypass_media = models.BooleanField(u'Bypass Media',null=False, blank=True)

    class Meta:
        db_table = 'device'
        verbose_name = u"Device"
        verbose_name_plural = u"Devices"
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs): # Procedimento para salvar codecs em string
        self.codec_inbound_string = get_codec_list(self.codec_inbound)
        self.codec_outbound_string = get_codec_list(self.codec_outbound)

        super(Device, self).save(*args, **kwargs)

class ProviderRule(models.Model):
    gateway = models.ForeignKey('Gateway')
    name = models.CharField('Nome',max_length=100,blank=False,null=False)
    cut = models.CharField('Cortar',max_length=100, blank=True)
    add = models.CharField('Adicionar',max_length=100, blank=True)    
    min_len = models.IntegerField(u'Mínimo de dígitos',null=False, blank=False)
    max_len = models.IntegerField(u'Máximo de dígitos',null=False, blank=False)

    class Meta:
        db_table = 'provider_rule'
        verbose_name = u"Regras de Discagem"
        verbose_name_plural = u"Regras de Discagem"
    def __unicode__(self):
        return ''

class Gateway(models.Model):
    name = models.CharField(u'Nome',max_length=80,unique=True,blank=False,null=False)
    provider = models.ForeignKey('Provider', verbose_name='Provedor')
    description = models.CharField(u'Descrição',max_length=80,null=False,blank=False,unique=True)
    register = models.BooleanField(u'Enviar register(?)',null=False, blank=True)
    accountcode = models.CharField(max_length=20, blank=True)
    callerid = models.CharField(u'CallerID',max_length=80, blank=True)
    callerid_number = models.CharField(u'CallerID (Número)',max_length=80, null=True, blank=True)
    fromuser = models.CharField(max_length=80, blank=True, verbose_name='From User')
    fromdomain = models.CharField(max_length=80, blank=True,verbose_name='From Domain')
    host = models.CharField(max_length=31, blank=True,null=True)
    permit = models.CharField(max_length=95, blank=True)
    deny = models.CharField(max_length=95, blank=True)
    port = models.CharField('Porta',max_length=5, blank=True,default='5060')
    password = models.CharField('Senha',max_length=80, null=True,blank=True)
    codec_inbound = models.CharField(max_length=80, null=True,verbose_name='Codec Inbound')
    codec_outbound = models.CharField(max_length=80, null=True,verbose_name='Codec Outbound')
    codec_inbound_string = models.CharField(max_length=200, null=True)
    codec_outbound_string = models.CharField(max_length=200, null=True)
    activecalls_limit = models.IntegerField(null=True,blank=True, verbose_name='Limite de chamadas ativas')
    calls_per_second = models.PositiveIntegerField('max calls per second', default=10, help_text="maximum calls per seconds allowed for this customer account.")
    class Meta:
        db_table = 'gateway'
        verbose_name = u"Gateway"
        verbose_name_plural = u"Gateways"
        
    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.codec_inbound_string = get_codec_list(self.codec_inbound)
        self.codec_outbound_string = get_codec_list(self.codec_outbound)
        super(Gateway, self).save(*args, **kwargs)
        self.name = 'prov%sgw%s' % (str(self.provider.id), str(self.id))
        super(Gateway, self).save(*args, **kwargs)

class Provider(models.Model):
    name = models.CharField(max_length=80, verbose_name='Nome')
    email = models.CharField(max_length=80, blank=True)
    phone_number = models.CharField(u'Telefone', max_length=20, blank=True)
    web_site = models.URLField(u'Site', blank=True)
    address =  models.TextField(u'Endereço', blank=True)
    postpaid_limit = models.DecimalField(null=True,blank=True, max_digits=8, decimal_places=2, verbose_name='Limite para Pos-Pago')
    # adicionar tabela de pagamentos customer_balance = models.DecimalField('customer balance', max_digits=12, decimal_places=6, default=0, help_text="Actual customer balance.")
    context = models.CharField(max_length=80, blank=True, default='provider')
    rate_group = models.ForeignKey('RateGroup', verbose_name='Tarifas')

    class Meta:
        db_table = 'provider'
        verbose_name = u"Provedor"
        verbose_name_plural = u"Provedores"
    def __unicode__(self):
        return self.name


class Dialrule(models.Model):
    dialrule_group = models.ForeignKey('DialruleGroup')
    name = models.CharField('Nome',max_length=100,blank=False,null=False)
    cut = models.CharField('Cortar',max_length=100, blank=True)
    add = models.CharField('Adicionar',max_length=100, blank=True)    
    min_len = models.IntegerField(u'Mínimo de dígitos',null=False, blank=False)
    max_len = models.IntegerField(u'Máximo de dígitos',null=False, blank=False)

    class Meta:
        db_table = 'dialrule'
        verbose_name = u"Regras de Discagem"
        verbose_name_plural = u"Regras de Discagem"
    def __unicode__(self):
        return self.name

class DialruleGroup(models.Model):
    name = models.CharField('Nome',max_length=100,unique=True,blank=False,null=False)
    class Meta:
        db_table = 'dialrule_group'
        verbose_name = u"Regras de Discagem"
        verbose_name_plural = u"Regras de Discagem"
    def __unicode__(self):
        return self.name    

class InboundRoute(models.Model):
    description = models.CharField(max_length=255, blank=False,null=False,verbose_name=u'Descrição')
    provider = models.ForeignKey(Provider,verbose_name='Provedor')
    area_id = models.IntegerField(null=True,blank=True)
    did = models.CharField(max_length=25,unique=True,verbose_name=u'Número de Entrada (DID)',null=False, blank=False)
    class Meta:
        db_table = 'inbound_route'
        verbose_name = u"Regra de Entrada"
        verbose_name_plural = u"Regras de Entrada"
    def __unicode__(self):
        return self.description

class InboundRule(models.Model):
    inbound_route = models.ForeignKey(InboundRoute,verbose_name='DID',null=False, blank=False)
    description = models.CharField(max_length=255,verbose_name=u'Descrição',null=False, blank=False)
    destination = models.CharField(max_length=25, verbose_name=u'Desvio',null=False, blank=False)
    weekdays = models.CharField(max_length=80, blank=True,verbose_name=u'Dias da Semana',)
    start = models.TimeField(null=False, blank=False,verbose_name=u'Início',default='00:00:00',)
    stop = models.TimeField(null=False, blank=False,verbose_name=u'Fim',default='23:59:59',)
    dayoff = models.BooleanField(null=False, blank=True,verbose_name=u'Feriados')
    specific_date = models.DateField(null=True, blank=True,verbose_name=u'Data Específica')
    class Meta:
        db_table = 'inbound_rule'
    def __unicode__(self):
        return self.description


TITLE_CHOICES = (
    ('priority', 'Prioridade'),
    ('price', 'Custo'),
)

class Lcr(models.Model):
    name = models.CharField('Nome',max_length=80,unique=True,blank=False,null=False)
    order = models.CharField('Ordem',max_length=40, blank=False,null=False,choices=TITLE_CHOICES)
    class Meta:
        db_table = 'lcr'
        verbose_name = u"LCR"
        verbose_name_plural = u"LCRs"
    def __unicode__(self):
        return self.name

class LcrProvider(models.Model):    
    lcr = models.ForeignKey(Lcr, null=False, blank=False)
    provider = models.ForeignKey(Provider,verbose_name='Provedor',null=False, blank=False)
    deactive = models.BooleanField(verbose_name='Desativo?',null=False, blank=True)
    priority = models.PositiveSmallIntegerField(verbose_name='Prioridade', null=True, blank=True)
    class Meta:
        db_table = 'lcr_provider'
        verbose_name = u"LCR - Provedor"
        verbose_name_plural = u"LCR - Provedores"
        ordering = ('priority', )
        
    def __unicode__(self):
        return ''

class RateTag(models.Model):
    description = models.CharField(u'Descrição',max_length=50,blank=False,null=False)
    tag = models.CharField('Tag',max_length=15,blank=False,null=False, unique=True)    
    class Meta:
        db_table = 'rate_tag'
        verbose_name = u"Tag - Tarifa"
        verbose_name_plural = u"Tags - Tarifas"
    def __unicode__(self):
        return self.tag

class Rate(models.Model):
    rate_group = models.ForeignKey('RateGroup',verbose_name='Grupo de tarifas', related_name='rates')
    prefix = models.CharField('Prefixo',max_length=50,blank=False,null=False)
    tag = models.ManyToManyField('RateTag', db_table='rategroup_ratetag', blank=True,null=True, verbose_name='Tags',)
    tags_string = models.CharField(max_length=200,blank=True,null=True)
    price = models.DecimalField(u'Preço', null=False, max_digits=10, decimal_places=5, default=0.0)
    min_time = models.IntegerField(u'Tempo mínimo', default=1, null=True)
    increment = models.IntegerField('Incremento', default=1, null=True)
    gateway = models.ForeignKey('Gateway', verbose_name=u'Tarifa específica para gateway', null=True, blank=True, help_text='Ao selecionar um gateway, a tarifa será específica para somente ele.')
    class Meta:
        db_table = 'rate'
        verbose_name = u"Tarifa"
        verbose_name_plural = u"Tarifas"
    def __unicode__(self):
        #return 'Prefixo: %s / Tags: %s' % (self.prefix, self.tag)
        return 'Prefixo: %s' % (self.prefix)

    def save(self, *args, **kwargs): # Procedimento para salvar codecs em string
        self.prefix = re.sub(' ', ',', self.prefix)
        super(Rate, self).save(*args, **kwargs)
        
RATE_TYPE = (
        ('provider', u'Provedor'),
        ('user', u'Usuário'),

    )
class RateGroup(models.Model):
    name = models.CharField(u'Descrição',max_length=80,unique=True,blank=False,null=False)
    grace_time = models.IntegerField(u'Grace Time', null=True, default=0)
    rate_type = models.CharField(choices=RATE_TYPE, max_length=15, verbose_name=u'Localização')
   
    class Meta:
        db_table = 'rate_group'
        verbose_name = u"Grupo de Tarifa"
        verbose_name_plural = u"Grupo de Tarifas"
   
    def __unicode__(self):
        return self.name

    def rates_count(self):
        return self.rates.count()
    rates_count.short_description = u'Número de Rates'

class Cdr(models.Model):
    customer = models.ForeignKey('Customer', db_index=True, null=True, blank=True,verbose_name='Cliente')
    uuid = models.CharField(max_length=80,verbose_name='UniqueID',null=True, unique=True)
    uuid_b = models.CharField(max_length=80,verbose_name='LegB UniqueID',blank=True,null=True)
    accountcode = models.CharField(max_length=80,verbose_name='Accountcode',blank=True,null=True)
    caller_id = models.CharField(max_length=80,verbose_name='Caller ID',blank=True,null=True)
    device = models.ForeignKey('Device', db_index=True, blank=True, null=True)
    destination_number = models.CharField(db_index=True, max_length=40,verbose_name='Destino',blank=True,null=True)
    lcr_name = models.CharField(max_length=40,verbose_name='LCR',blank=True,null=True)
    rate_group = models.CharField(max_length=40,verbose_name='Tarifa',blank=True,null=True)
    start_time = models.DateTimeField(db_index=True, blank=True,null=True, verbose_name=u'Data')
    end_time = models.DateTimeField(blank=True,null=True, verbose_name=u'Fim')
    billsec = models.IntegerField(verbose_name='Real Billsec', null=True)
    duration = models.CharField(max_length=30,verbose_name=u'Duração Total',blank=True,null=True)
    provider = models.ForeignKey('Provider', db_index=True, null=True, blank=True, verbose_name='Provedor')  
    gateway = models.ForeignKey('Gateway', db_index=True, blank=True, null=True)
    hangup_cause = models.CharField(max_length=40,verbose_name='Hangup cause',blank=True,null=True)
    hangup_cause_q850 = models.CharField(max_length=10,verbose_name='Hangup cause Q850',blank=True,null=True)
    remote_media_ip = models.CharField(max_length=20,verbose_name='Remote Media',blank=True,null=True)
    sip_received_ip = models.CharField(max_length=20,verbose_name='Received IP',blank=True,null=True)
    endpoint_disposition = models.CharField(max_length=40,verbose_name='Disposition',blank=True,null=True)
    hangup_disposition = models.CharField(max_length=40,verbose_name='LCR name',blank=True,null=True)
    read_codec = models.CharField(max_length=80,verbose_name='Read codec',blank=True,null=True)
    write_codec = models.CharField(max_length=80,verbose_name='Write codec',blank=True,null=True)
    cdr_object_id = models.CharField(max_length=80,verbose_name='Mongodb CDR ID',blank=True,null=True)
    user_billsec = models.IntegerField(verbose_name='Customer Billsec', null=True)
    provider_billsec = models.IntegerField(verbose_name='Provider Billsec', null=True)
    provider_cost = models.DecimalField(max_digits=11, decimal_places=5, verbose_name='Valor Provedor', default="0", null=True)
    user_cost = models.DecimalField(max_digits=11, decimal_places=5, verbose_name='Valor Usuário', default="0", null=True)   
    provider_rate_name = models.CharField(max_length=40,verbose_name='Provider rate name',blank=True,null=True)
    provider_rate_prefix = models.CharField(max_length=30,verbose_name='Provider rate prefix',blank=True,null=True)
    provider_rate_price =  models.DecimalField(max_digits=10,decimal_places=4,verbose_name='Valor provedor',blank=True,null=True)
    provider_rate_min_time = models.IntegerField(verbose_name='Provider rate minimal time', null=True)
    provider_rate_increment = models.IntegerField(verbose_name='Provider rate increment', null=True)
    provider_rate_tags = models.CharField(max_length=100,verbose_name='Provider rate tags',blank=True,null=True)
    user_rate_name = models.CharField(max_length=40,verbose_name='User rate name',blank=True,null=True)
    user_rate_prefix = models.CharField(max_length=30,verbose_name='User rate prefix',blank=True,null=True)
    user_rate_price =  models.DecimalField(max_digits=10,decimal_places=4,verbose_name=u'Valor Usuário',blank=True,null=True)
    user_rate_min_time = models.IntegerField(verbose_name='User rate minimal time', null=True)
    user_rate_increment = models.IntegerField(verbose_name='User rate increment', null=True)
    user_rate_tags = models.CharField(max_length=100,verbose_name='User rate tags',blank=True,null=True)
    user_rate_gracetime = models.IntegerField(u'User gracetime', null=True, default=0)
    provider_rate_gracetime = models.IntegerField(u'Provider gracetime', null=True, default=0)
    progressmedia_time = models.CharField(max_length=10,verbose_name='PDD',blank=True,null=True)
    hangup_commentary = models.CharField(max_length=100,verbose_name='Hangup Commentary',blank=True,null=True)
    commentary = models.CharField(max_length=100,verbose_name='Commentary',blank=True,null=True)
    sip_via_host = models.CharField(max_length=20,verbose_name='SIP via Host',blank=True,null=True)
    sip_to_port = models.CharField(max_length=15,verbose_name='SIP Port',blank=True,null=True)
    sip_user_agent = models.CharField(max_length=80,verbose_name='SIP User Agent',blank=True,null=True)
    sip_contact_uri = models.CharField(max_length=80,verbose_name='SIP Contact URI',blank=True,null=True)


    class Meta:
        db_table = 'cdr'
        verbose_name = u'CDR'
        verbose_name_plural = u'CDR' 



class CdrTries(models.Model):
    cdr = models.ForeignKey('Cdr',null=True,blank=True)
    uuid_a = models.CharField(max_length=80,verbose_name='LegA UniqueID',blank=True,null=True)
    uuid_b = models.CharField(max_length=80,verbose_name='LegB UniqueID',blank=True,null=True)
    gateway = models.ForeignKey('Gateway', blank=True, null=True)
    provider_rate_name = models.CharField(max_length=40,verbose_name='Provider rate name',blank=True,null=True)
    start_time = models.DateTimeField(blank=True,null=True, verbose_name=u'Início')
    progressmedia_time = models.CharField(max_length=10,verbose_name='PDD',blank=True,null=True)
    endpoint_disposition = models.CharField(max_length=40,verbose_name='Disposition',blank=True,null=True)
    hangup_disposition = models.CharField(max_length=40,verbose_name='hangup_disposition',blank=True,null=True)
    hangup_cause = models.CharField(max_length=40,verbose_name='Hangup cause',blank=True,null=True)
    hangup_cause_q850 = models.CharField(max_length=10,verbose_name='Hangup cause Q850',blank=True,null=True)

    class Meta:
        db_table = 'cdr_tries'
        

class CustomerBalance(models.Model):
    customer = models.ForeignKey('Customer', null=True, blank=True,verbose_name='Cliente')
    datetime = models.DateTimeField(blank=True,null=True, verbose_name=u'Data')
    provider = models.ForeignKey('Provider', null=True, blank=True, verbose_name='Provedor')  
    gateway = models.ForeignKey('Gateway', blank=True, null=True)
    total =  models.DecimalField(max_digits=20,decimal_places=4,verbose_name=u'Valor Usuário',blank=True,null=True)

    class Meta:
        db_table = 'customer_balance'
        verbose_name = u"Balanço"
        verbose_name_plural = u"Balanço"
    def __unicode__(self):
        return self.name


'''
    Function: Return the customer by user id
'''

def get_customer_by_user(u):
    obj = CustomUsers.objects.filter(user=u)
    if not obj:
        return False

    else:
        return [e.customer for e in obj][0]

'''
    Function: Get codec by id
'''

def get_codec_list(u):
    codecs_string = re.sub('[u,\'\[\]]', '', u)
    codecs_list = codecs_string.split()
    codecs = ''

    for obj in codecs_list:
        res = Codec.objects.filter(pk=obj)
        if res:
            codecs += [res.codec for res in res][0]            
            codecs += ','

    if (len(codecs) > 1): # Remove ultima virgula
        codecs = codecs[:-1]
    
    return codecs

