# -*- coding:utf-8 -*-

from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseNotFound,HttpResponseRedirect
from django.shortcuts import (render, render_to_response, get_object_or_404, redirect)
from ipsafe.core.models import Device, Customer, Provider, Blacklist, Gateway

from ipsafe.freeswitch.esl_functions import FSinfo

import os

def render_to_file(template, filename, context):
    open(filename, "w").write(render_to_string(template, context))

def parse_devices(request):
	context = {}
	devices = Device.objects.all()
	for obj in devices:
		values = Customer.objects.filter(pk=obj.customer.id)
		obj.userinfo = values

	context['list'] = devices
	render_to_file('devices.xml', '/usr/local/freeswitch/conf/directory/default/devices.xml', context)

	fs = FSinfo()
	fs.getReloadxml()
	fs.getReloadACL()
	fs.getRestartSofiaAll()
	return


def parse_providers(request):
	context = {}
	gateways = Gateway.objects.all()
	for obj in gateways:
		print obj
		values = Provider.objects.filter(pk=obj.provider.id)
		obj.provider_values = values

	context['list'] = gateways
	render_to_file('gateways.xml', '/usr/local/freeswitch/conf/sip_profiles/external/gateways.xml', context)

	fs = FSinfo()
	fs.getReloadxml()
	fs.getReloadACL()
	fs.getRestartSofiaAll()	
	return

def parse_blacklist(request):
	context = {}
	list = Blacklist.objects.all()
	context['list'] = list
	render_to_file('blacklist.list', '/usr/local/freeswitch/conf/blacklist.list', context)
	render_to_file('blacklist.conf.xml', '/usr/local/freeswitch/conf/autoload_configs/blacklist.conf.xml', {})