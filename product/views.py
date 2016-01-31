from django.views.generic import DetailView, ListView, FormView, View
from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.contrib.messages import (get_messages, success, error, ERROR,
                                     add_message)
from product.models import Product, Like
from product.forms import CommentForm


class ProductDetailView(DetailView):
    """
    Product detail page
    """
    context_object_name = "product"
    model = Product

    def get_context_data(self, **kwargs):
        ctx = super(ProductDetailView, self).get_context_data(**kwargs)
        ctx['form'] = CommentForm(initial={'product': self.object.id})
        ctx['like'] = self.request.user.is_authenticated() and \
            Like.objects.filter(product=self.object,
                                user=self.request.user).exists()
        ctx['messages'] = get_messages(self.request)
        return ctx


class ProductListView(ListView):
    """
    Product List Page with pagination
    """
    model = Product
    paginate_by = 5


class CreateCommentView(FormView):
    form_class = CommentForm
    _success_message = 'Comment was added succesfully.'

    def form_valid(self, form):
        form.save()
        success(self.request, self._success_message)
        return redirect(form.cleaned_data['product'].get_absolute_url())

    def form_invalid(self, form):
        for i in form.errors:
            for message in form.errors[i]:
                add_message(self.request, ERROR, message, extra_tags=i)
        return redirect(form.cleaned_data['product'].get_absolute_url())


class ProductLikeView(View):
    """
    View for product's liking
    """
    _success_message = 'You like this product.'
    _error_message = 'You have already liked this product.'

    def get(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['slug'])
        if Like.objects.filter(product=product, user=self.request.user
                               ).exists():
            error(self.request, self._error_message)
        else:
            Like(product=product, user=self.request.user).save()
            success(self.request, self._success_message)
        return redirect(product.get_absolute_url())
