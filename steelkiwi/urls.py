from django.views.generic import RedirectView
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', RedirectView.as_view(url='product-list'), name='home'),
    url(r'^products/', include('product.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
