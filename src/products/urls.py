from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import ProductDetailView, ProductListView,VariationDetailView,VariationListView

urlpatterns = [
    # Examples:
    url(r'^$', ProductListView.as_view(), name='products'),
    url(r'^(?P<pk>\d+)/inventory/$', VariationDetailView.as_view(), name='product_inventory'),
    url(r'^(?P<pk>\d+)$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^inventories/$', VariationListView.as_view(), name='variations_list'),
    # url(r'^(?P<pk>\d+)$', 'products.views.product_detail_view_func', name='product_detail_view_func'),
]