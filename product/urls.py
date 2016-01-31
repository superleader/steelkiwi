from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from product.views import (ProductListView, ProductDetailView,
                           CreateCommentView, ProductLikeView)


urlpatterns = patterns('',
                       url(r'^comment/', CreateCommentView.as_view(),
                           name='comment'),
                       url(r'^(?P<slug>[a-zA-Z0-9_\-]*)/$',
                           ProductDetailView.as_view(),
                           name='product-detail'),
                       url(r'^(?P<slug>[a-zA-Z0-9_\-]*)/like/$',
                           login_required(ProductLikeView.as_view()),
                           name='like-product'),
                       url(r'^$', ProductListView.as_view(),
                           name='product-list'),
                       )
