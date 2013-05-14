from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('BuckIt.buckitapp.views',
    # Examples:
    # url(r'^$', 'BuckIt.views.home', name='home'),
    # url(r'^BuckIt/', include('BuckIt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'login'),
    url(r'^login/(?P<errorcode>\d+)/$', 'login'),
    url(r'^login/$', 'login'),
    url(r'^home/$', 'home'),
    url(r'^profile/(?P<userid>\w+)/$', 'profile'),
    url(r'^search/$', 'search'),
)

urlpatterns += patterns('',
    url(r'', include('social_auth.urls')),
)