from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from product.models import Product
from product.views import CreateCommentView, ProductLikeView


class ProductTest(TestCase):
    _product_name = u'product name'
    _product_description = u'product description'
    _product_slug = u'slug'
    _product_price = 1
    _user_password = u'password'
    _user_email = u'tt@tt.tt'

    def setUp(self):
        self.client = Client()
        self.product = Product(name=self._product_name,
                               slug=self._product_slug,
                               price=self._product_price,
                               description=self._product_description)
        self.product.save()
        self.user = User.objects.create_user(self._user_email,
                                             self._user_email,
                                             self._user_password)

    def assert_message_contains(self, response, text, level=None):
        """
        Asserts that there is exactly one message containing the given text.
        """
        messages = response.context['messages']
        matches = [m for m in messages if text in m.message]
        if len(matches) == 1:
            msg = matches[0]
            if level is not None and msg.level != level:
                self.fail('There was one matching message but with different'
                          'level: %s != %s' % (msg.level, level))
            return
        elif len(matches) == 0:
            messages_str = ", ".join('"%s"' % m for m in messages)
            self.fail('No message contained text "%s", messages were: %s' %
                      (text, messages_str))
        else:
            self.fail('Multiple messages contained text "%s": %s' %
                      (text, ", ".join(('"%s"' % m) for m in matches)))

    def test_product_detail(self):
        """
        Test /products/<slug>/ page
        """
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product_detail.html')
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.description)
        self.assertContains(response, self.product.price)
        return response

    def test_product_comment(self):
        url = reverse('comment')
        """
        Test product's comment creating
        """
        # Send request with empty text field
        response = self.client.post(url, {'product': self.product.id},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assert_message_contains(response, 'This field is required.')

        # Send request with params
        response = self.client.post(url, {'product': self.product.id,
                                          'text': 'test'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assert_message_contains(response,
                                     CreateCommentView._success_message)

    def test_product_like(self):
        """
        Test product's liking
        """
        url = reverse('like-product', args=[self.product.slug])
        # Send request with unauthorised user
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)

        self.client.login(username=self._user_email,
                          password=self._user_password)

        # Like firstly succesfully
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assert_message_contains(response,
                                     ProductLikeView._success_message)

        # Like firstly succesfully with error
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assert_message_contains(response,
                                     ProductLikeView._error_message)
