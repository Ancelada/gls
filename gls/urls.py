from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^models/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^', include('mainapp.urls')),
    url(r'^', include('login.urls')),
    url(r'^', include('report.urls')),
]
