# -*- coding:utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import *
import re

###############################################################
########## Snippet to require at least one inline in form #####
###############################################################

from django.forms.models import BaseInlineFormSet

class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

""" End snippet """

###############################################################
###############################################################


class CustomerForm(ModelForm):
    class Meta:
        model = Customer        
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['rate_groups'].queryset = RateGroup.objects.filter(rate_type='user')

class ProviderForm(ModelForm):
    class Meta:
        model = Provider        
    def __init__(self, *args, **kwargs):
        super(ProviderForm, self).__init__(*args, **kwargs)
        self.fields['rate_group'].queryset = RateGroup.objects.filter(rate_type='provider')


class CdrForm(ModelForm):
    class Meta:
        model = Cdr
        fields = ('customer','device','provider','gateway',)


class DialrulesForm(ModelForm):
    class Meta:
        model = Dialrule
        fields = ('name','cut','add','min_len','max_len',)
    def __init__(self, *args, **kwargs):
        super(DialrulesForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = "span10"
        self.fields['cut'].widget.attrs['class'] = "span8"
        self.fields['add'].widget.attrs['class'] = "span8"
        self.fields['min_len'].widget.attrs['class'] = "span3"
        self.fields['max_len'].widget.attrs['class'] = "span3"


class ProviderRulesForm(ModelForm):
    class Meta:
        model = ProviderRule
        fields = ('name','cut','add','min_len','max_len',)
    def __init__(self, *args, **kwargs):
        super(ProviderRulesForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = "span10"
        self.fields['cut'].widget.attrs['class'] = "span8"
        self.fields['add'].widget.attrs['class'] = "span8"
        self.fields['min_len'].widget.attrs['class'] = "span3"
        self.fields['max_len'].widget.attrs['class'] = "span3"


class LcrProviderForm(ModelForm):    
    #priority = forms.CharField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = LcrProvider
    def __init__(self, *args, **kwargs):
        super(LcrProviderForm, self).__init__(*args, **kwargs)        
        #self.fields['priority'].widget = forms.HiddenInput()
        
class DeviceForm(ModelForm):
    password = forms.CharField(min_length=8, required=False, label='Senha')
    codec_inbound = forms.MultipleChoiceField(choices=Codec.objects.all().values_list('id','codec',),)
    codec_outbound = forms.MultipleChoiceField(choices=Codec.objects.all().values_list('id','codec',),)

    class Meta:
        model = Device

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['codec_inbound'].initial = [c.pk for c in Codec.objects.filter(codec__in=['G722','PCMA','PCMU','GSM','G729'])]
        self.fields['codec_outbound'].initial = [c.pk for c in Codec.objects.filter(codec__in=['G729','PCMA','PCMU','GSM'])]            


WEEKDAYS = (
         ('1','Segunda'),
         ('2',u'Terça'),
         ('3','Quarta'),
         ('4','Quinta'),
         ('5','Sexta'),
         ('6',u'Sábado'),
         ('0','Domingo'),
)


class GatewaysForm(ModelForm):
    password = forms.CharField(min_length=8, required=False, label='Senha')
    codec_inbound = forms.MultipleChoiceField(choices=Codec.objects.all().values_list('id','codec',),)
    codec_outbound = forms.MultipleChoiceField(choices=Codec.objects.all().values_list('id','codec',),)    

    class Meta:
        model = Gateway

    def __init__(self, *args, **kwargs):
        super(GatewaysForm, self).__init__(*args, **kwargs)
        self.fields['codec_inbound'].initial = [c.pk for c in Codec.objects.filter(codec__in=['G722','PCMA','PCMU','GSM','G729'])]
        self.fields['codec_outbound'].initial = [c.pk for c in Codec.objects.filter(codec__in=['G729','PCMA','PCMU','GSM'])]        

class RatesForm(ModelForm):
    #tag = forms.MultipleChoiceField(label='Tags', choices=CHOICES, required=False)
    #tag = forms.MultipleChoiceField(choices=RateTag.objects.all().values_list('id', 'tag',), required=False)
    class Meta:
        model = Rate
    def __init__(self, *args, **kwargs):
        super(RatesForm, self).__init__(*args, **kwargs)
        self.fields['tag'].help_text = ''

class InboundRulesForm(ModelForm):
    weekdays = forms.MultipleChoiceField(label='Dias da Semana',choices=WEEKDAYS, widget=forms.CheckboxSelectMultiple(),)
    class Meta:
        model = InboundRule
