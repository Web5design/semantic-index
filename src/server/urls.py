from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','server.views.index'),
    url(r'^index', 'server.views.index'),
	url(r'^parse', 'server.views.parse'),
	url(r'^answer', 'server.views.answer'),
	url(r'^visualize', 'server.views.visualize'),
)
