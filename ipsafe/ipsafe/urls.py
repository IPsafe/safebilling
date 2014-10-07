from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import *

from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()
urlpatterns = patterns('',
    (r'^report/$', admin.site.admin_view(report)),
    (r'^report/results/$', admin.site.admin_view(reportResults)),
    (r'^report/details/$', admin.site.admin_view(reportDetails)),

	url(r'^api/getProviderRateType/(?P<provider>\d+)$', 'ipsafe.core.views.getProviderRateType', name='getProviderRateType'),

	url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(admin.site.urls)),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
   urlpatterns += patterns('',
       (r'^static/(?P<path>.*)$', 'django.views.static.serve',
       {'document_root': settings.STATIC_ROOT}),
   )

#handler403 = 'mysite.views.my_custom_permission_denied_view'
#handler404 = 'mysite.views.my_custom_permission_denied_view'