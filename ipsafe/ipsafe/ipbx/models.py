from django.db import models


class Conference(models.Model):
    user = models.ForeignKey(User)
    customer = models.ForeignKey(Customers, null=True)
    name = models.CharField(verbose_name=u'Descrição',max_length=80,null=False,blank=False)
    number = models.CharField(verbose_name=u'Código', max_length=80,unique=True, blank=False, null=False)
    class Meta:
        db_table = 'conference'
        verbose_name = u"Sala de Conferência"
        verbose_name_plural = u"Salas de Conferências"
    def __unicode__(self):
        return self.name
    

class PickupGroups(models.Model):
    user = models.ForeignKey(User)
    customer = models.ForeignKey(Customers, null=True)
    name = models.CharField('Nome',max_length=100,unique=True,blank=False,null=False)
    class Meta:
        db_table = 'pickup_groups'
        verbose_name = u"Grupo de Captura"
        verbose_name_plural = u"Grupos de Captura"
    def __unicode__(self):
        return self.name


class QueueMembers(models.Model):
    queues = models.ForeignKey('Queues', null=True, blank=True)
    interface = models.CharField('Ramal',max_length=128,null=False, blank=False,)
    order = models.IntegerField(null=False, blank=False,verbose_name='Ordem',)
    paused = models.CharField(max_length=5, null=True, blank=True,verbose_name='Desativar?', default=None)
    class Meta:
        db_table = 'queue_members'
        verbose_name = u"Membros"
        verbose_name_plural = u"Membros"
        ordering = ['order']

class Queues(models.Model):
    user = models.ForeignKey(User)
    customer = models.ForeignKey(Customers, null=True)
    description = models.CharField(u'Descrição', max_length=100, blank=False,null=False)
    name = models.CharField(u'Código',max_length=128,unique=True,blank=False,null=False)
    class Meta:
        db_table = 'queues'
        verbose_name = u"Fila"
        verbose_name_plural = u"Filas"
    def __unicode__(self):
        return self.description
    def save(self, *args, **kwargs):
        QueueMembers.objects.filter(queues=self.id).update(queue_name=self.name)
        super(Queues, self).save(*args, **kwargs)


class Lock(models.Model):
    user = models.ForeignKey(User)
    customer = models.ForeignKey(Customers, null=True)
    description= models.CharField(max_length=80)
    login = models.CharField(max_length=5)
    password = models.CharField(max_length=5)


class LockDevices(models.Model):
    device = models.ForeignKey(Devices)
    lock = models.ForeignKey(Lock, null=True)

class VoicemailUsers(models.Model):
    user = models.ForeignKey(User)
    context = models.CharField(max_length=50)
    mailbox = models.IntegerField()
    password = models.CharField(max_length=4)
    fullname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    pager = models.CharField(max_length=50)
    stamp = models.DateTimeField()
    class Meta:
        db_table = 'voicemail_users'