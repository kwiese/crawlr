"""crawlrProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from crawlr import views

urlpatterns = [
    url('', include('social_django.urls', namespace='social')),
    url(r'^application/', include('crawlr.urls')),
    url(r'^FAQ/', TemplateView.as_view(template_name='FAQ.html')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^members/', views.members, name='members'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/$', views.login, name="login"),
    url(r'^$', views.home, name='home'),
]

#########################################################################################33333#########33

# from django.conf.urls import url, include
# from django.contrib import admin
# from django.contrib.auth import views as auth_views
# sys.path.insert(1, os.path.join(sys.path[0], '..'))
# from crawlr import views as core_views
#
# urlpatterns = [
#     url(r'^$', core_views.home, name='home'),
#     url(r'^login/$', auth_views.login, name='login'),
#     url(r'^logout/$', auth_views.logout, name='logout'),
#     url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),  # <--
#     url(r'^admin/', admin.site.urls),
# ]

#########################################################################################33333#########33

# from django.conf.urls import url, include
# from django.contrib import admin
# from django.views.generic import TemplateView
# import oauth2client.contrib.django_util.site as django_util_site
# import os,sys
# import django.contrib.auth.views
# sys.path.insert(1, os.path.join(sys.path[0], '..'))
# from crawlr import views
#
# urlpatterns = [
#     url(r'^application/', include('crawlr.urls')),
#     url(r'^FAQ/', TemplateView.as_view(template_name='FAQ.html')),
#     url(r'^$', views.index, name='index'),
#     url(r'^oauth2callback', views.auth_return, name='auth_return'),
#     url(r'^login', django.contrib.auth.views.login, name="login"),
#     #url("^soc/", include("social_django.urls", namespace="social"))
# ]
#urlpatterns = [url(r'^application/', TemplateView.as_view(template_name='index.html')), url(r'^$', TemplateView.as_view(template_name='index_home.html'))]

######################################################################################################

# from django.conf import urls
# from django.contrib import admin
# import django.contrib.auth.views
# import os,sys
# sys.path.insert(1, os.path.join(sys.path[0], '..'))
# from crawlr import views
#
# import oauth2client.contrib.django_util.site as django_util_site
#
#
# urlpatterns = [
#     urls.url(r'^$', views.index),
#     urls.url(r'^profile_required', views.get_profile_required),
#     urls.url(r'^profile_enabled', views.get_profile_optional),
#     urls.url(r'^admin/', urls.include(admin.site.urls)),
#     urls.url(r'^login', django.contrib.auth.views.login, name="login"),
#     urls.url(r'^oauth2/', urls.include(django_util_site.urls)),
# ]
