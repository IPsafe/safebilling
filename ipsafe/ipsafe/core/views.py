# -*- coding:utf-8 -*-
from django.http import HttpResponse, HttpResponseNotFound,HttpResponseRedirect
from django.shortcuts import (render, render_to_response, get_object_or_404, redirect)
from datetime import datetime, timedelta, date, time
from models import *
from forms import CdrForm
from django.template import RequestContext,loader, Context
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
#from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import json
from django.core.paginator import Paginator

@login_required(login_url='/login/')
def report(request):
    context = {}
    form = CdrForm(request.POST or None)
    context['form'] = form
    context['view'] = 'report'
    context = RequestContext(request, context)

    return render(request, 'reportform.html', context)

@login_required(login_url='/login/')
def reportResults(request):
    context = {}    
    cdr = {}
    template_name = 'report.html'    

    if request.POST:
        request.session['qs'] = request.POST

    postData = request.session['qs']
    page = request.GET.get('page')

    ''' CDR QUERY '''
    args = []

    if (postData['start_time'] != ''):
        args.append(Q(start_time__gte = datetime.strptime(postData['start_time'], '%d/%m/%Y %H:%M:%S')),)
        context['start_time'] = postData['start_time']
    else:
        args.append(Q(start_time__gte = date.today()),)
        context['start_time'] = str(date.today())
            
    if (postData['end_time'] != ''):
        args.append(Q(start_time__lte = datetime.strptime(postData['end_time'], '%d/%m/%Y %H:%M:%S')),)
        context['end_time'] = postData['end_time']     
    
    if (postData['device'] != ''):
        args.append(Q(device = postData['device']))
        context['device'] = postData['device']

    if (postData['customer'] != ''):
        args.append(Q(customer = postData['customer']))
        context['customer'] = postData['customer']

    if (postData['gateway'] != ''):
        args.append(Q(gateway = postData['gateway']))
        context['gateway'] = postData['gateway']

    if (postData['provider'] != ''):
        args.append(Q(provider = postData['provider']))
        context['provider'] = postData['provider']

    cdr = Cdr.objects.filter(*args).order_by('-start_time').annotate(user_cost_total=Sum('user_cost'), provider_cost_total=Sum('provider_cost'))

    cost_total = {}
    cost_total = Cdr.objects.filter(*args).extra(select={
            'user_cost_total': 'SUM(user_cost)', 
            'provider_cost_total': 'SUM(provider_cost)',
            'profit_total': 'SUM(user_cost) - SUM(provider_cost)',
            'billsec_total': 'DATE_FORMAT(SEC_TO_TIME(SUM(billsec)), "%%H:%%m:%%S")',
            'billsec_sum': 'SUM(billsec)',
        }).values(
                'user_cost_total', 
                'provider_cost_total',
                'profit_total',
                'billsec_total',
                'billsec_sum',
            )[0]

    cost_total['billsec_total'] = str(timedelta(seconds=int(cost_total['billsec_sum'])))

    page = request.GET.get('page', 1)

    paginator = Paginator(cdr, 50)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    print 'count: %s' % str(paginator.count)
    print 'num pages: %s' % str(paginator.num_pages)

    for obj in page_obj:
        obj.billsec = str(timedelta(seconds=int(obj.billsec)))
        obj.profit = (obj.user_cost - obj.provider_cost)

  
    context['page_obj'] = page_obj
    context['cost_total'] = cost_total
    context['paginator'] = paginator
    context['request'] = request
    context['count'] = paginator.count
    context['view'] = 'reportResults'

    '''

    EXPORT CSV FILE
    
    '''
    if 'csv' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'
        template_name = 'csv.html'
        t = loader.get_template('csv.html')
        c = Context({
            'cdr': cdr,
            })
        response.write(t.render(c))
        return response
    
    '''
    END - EXPORT CSV
    '''
    
    return render(request, template_name, context)


#######################################################################################
####################################################################################### 

@login_required(login_url='/login/')
def reportDetails(request):
    context = {}
    cdr = {}
    template_name = 'reportdetails.html'

    if 'uuid' in request.GET:
        get_uuid = request.GET['uuid']

    cdr = Cdr.objects.filter(uuid=get_uuid)
    
    for obj in cdr:
        cdr.details = CdrTries.objects.filter(uuid_a = get_uuid)

        if obj.billsec:
            obj.billsec = str(timedelta(seconds=int(obj.billsec)))
    	obj.profit = (obj.provider_cost - obj.user_cost)
            
    context['cdr'] = cdr

    
    return render(request, template_name, context)

#######################################################################################
####################################################################################### 

# Retorna o tipo de rate configurado no provedor (usado para mostrar/ocultar campo rate_group na tela de gateway
    
@login_required(login_url='/login/')
def getProviderRateType(request, provider):
    response_data = {}
    if provider:    
        res = Provider.objects.filter(id=int(provider))
        for obj in res:
            response_data['rate_type'] = str(obj.rate_type)
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")
