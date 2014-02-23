import os
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from bountyfulcoinsapp.views import *

site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'bountyfulcoins.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       # Browsing
                       url(r'^$', main_page),
                       url(r'^popular/$', popular_page),
                       url(r'^user/(\w+)/$', user_page),
                       url(r'^tag/([^\s]+)/$', tag_page),
                       url(r'^tag/$', tag_cloud_page),
                       url(r'^search/$', search_page),
                       url(r'^about/$', about_page),

                       # Session and user management
                       url(r'^login/$', 'django.contrib.auth.views.login'),
                       url(r'^logout/$', logout_page),
                       url(r'^register/$', register_page),
                       url(r'^register/success/$',
                           TemplateView.as_view(template_name="registration/register_success.html")),

                       # Content Management
                       url(r'^save/$', bounty_save_page),
                       url(r'^vote/$', bounty_vote_page),

                       # Site Media
                       url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': site_media}),

                       # Django CMS Admin Page
                       url(r'^admin/', include(admin.site.urls)),
                       )
