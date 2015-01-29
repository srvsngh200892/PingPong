from django.conf.urls import patterns, include, url
from v0.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     #url(r'^$', 'pingpong.views.home', name='home'),
    #url(r'^blog/', include('blog.urls')),
    #url (r'^$', include('v0.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'v0.views.auth_login', name='user_login'),
    url(r'^logout/$', 'v0.views.user_logout', name='user_logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
    url(r'^game/$', game),
    url(r'^game/attacker/(?P<gm_id>[a-zA-Z0-9]+)/$', 'v0.views.attacker_game', name='attacker_game'),
    url(r'^game/defender/(?P<gm_id>[a-zA-Z0-9]+)/$', 'v0.views.defender_game', name='defender_game'),
) 


