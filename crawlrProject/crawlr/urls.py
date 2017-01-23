from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [url(r'^/application/', TemplateView.as_view(template_name='index.html')) ,url(r'^$', TemplateView.as_view(template_name='index_home.html')),]
