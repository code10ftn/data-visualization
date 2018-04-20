from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^load_data', views.load_data, name="load_data"),
    url(r'^display_data/(?P<plugin_id>([a-z]+|[_])+)$', views.display_data, name="display_data"),
    url(r'^filter_data', views.filter_data, name="filter_data"),
    url(r'^search_data', views.search_data, name="search_data")
]
