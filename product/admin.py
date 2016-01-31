from product.models import Product, Comment, Like

from django.contrib.admin import site

#site.register()
site.register((Product, Comment, Like,))
