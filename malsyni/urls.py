from django.conf.urls import patterns, include, url
from malsyni.views import Login, Logout, Loggedin, Invalid, Nidurstodur, Rannsakandastjb
from malsyni.myndraent import Graf
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', Login.as_view()),
    url(r'^accounts/auth/$', Login.as_view()),
    url(r'^accounts/logout/$', Logout.as_view()),
    url(r'^accounts/loggedin/$', Loggedin.as_view()),
    url(r'^accounts/invalid/$', Invalid.as_view()),
    url(r'^malsyni/nidurstodur/$', Nidurstodur.as_view()),
    url(r'^malsyni/stjornbord/$', Rannsakandastjb.as_view()),
    url(r'^malsyni/graf/$', 'malsyni.views.graf'),
    url(r'^charts/(?P<dbgildi>\d+(?:\.\d+)?)/(?P<stbdbgildi>\d+(?:\.\d+)?)/(?P<malsyni>\d+(?:\.\d+)?)/(?P<stbmalsyni>\d+(?:\.\d+)?)/(?P<sulur>\d+(?:\.\d+)?)/(?P<ylabel>\d+(?:\.\d+)?)/(?P<xlabel>\d+(?:\.\d+)?)/(?P<titill>\d+(?:\.\d+)?)/(?P<xticks>\d+(?:\.\d+)?)/graf/$', Graf.as_view()),
)

