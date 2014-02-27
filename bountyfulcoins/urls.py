import os

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from bountyfulcoinsapp import views

site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'bountyfulcoins.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Browsing
    url(r'^$', views.main_page, name='main_page'),
    url(r'^popular/$', views.popular_page, name='popular'),
    url(r'^user/(\w+)/$', views.user_page, name='user_page'),
    url(r'^tag/([^\s]+)/$', views.tag_page, name='tag'),
    url(r'^tag/$', views.tag_cloud_page, name='tag_cloud'),
    url(r'^about/$', views.about_page, name='about'),

    # Session and user management
    # url(r'^login/$', 'django.contrib.auth.views.login'),
    # url(r'^logout/$', logout_page),
    # url(r'^register/$', register_page),
    # url(r'^register/success/$', TemplateView.as_view(
    #     template_name="registration/register_success.html")),

    # Content Management
    url(r'^bounty/$', login_required(views.BountyCreate.as_view()),
        name='create_bounty'),
    url(r'^bounty/(?P<pk>\d+)$', login_required(views.BountyChange.as_view()),
        name='change_bounty'),
    url(r'^search/$', views.search_page, name='search'),
    url(r'^vote/$', views.bounty_vote_page),

    # Site Media
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': site_media}),

    # django registration
    url(r'^register/$', views.RegistrationView.as_view(),
        name='registration_register'),
    url(r'', include('registration.backends.default.urls')),

    # Django Admin Page
    url(r'^admin/', include(admin.site.urls)),
)
