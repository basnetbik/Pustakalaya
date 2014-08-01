from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'pustakalaya.views.home', name='home'),
    url(r'^add_to_wishlist/$', 'pustakalaya.views.add_to_wishlist'),
    url(r'^signup/$', 'pustakalaya.views.signup'),
    url(r'^login/$', 'pustakalaya.views.login'),
    url(r'^test/$', 'pustakalaya.views.test'),
    url(r'^logout/$', 'pustakalaya.views.logout'),
    url(r'^booksearch/$', 'pustakalaya.booksearch.search'),
#    url(r'^recommended/$', 'pustakalaya.booksearch.recommended'),
    # url(r'^CityApp/', include('CityApp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
