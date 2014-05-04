from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twitter_like.views.home', name='home'),
    # url(r'^twitter_like/', include('twitter_like.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^twitter_like/', include('twitter_like_app.urls',namespace='twitter_like')),
    url(r'^$',include('twitter_like_app.urls') ),
)
