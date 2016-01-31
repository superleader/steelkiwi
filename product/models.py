from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.db.models import (Model, CharField, SlugField, TextField,
                              DecimalField, DateTimeField, ForeignKey,
                              PositiveIntegerField)


class Product(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True)
    description = TextField()
    price = DecimalField(max_digits=19, decimal_places=2)
    created_at = DateTimeField(default=datetime.now)
    modified_at = DateTimeField(auto_now=True)
    likes = PositiveIntegerField(default=0)

    def count_likes(self):
        self.likes += 1
        self.save()

    def decrease_likes(self):
        self.likes -= 1
        self.save()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def last_comments(self):
        return self.comments.filter(created_at__gt=datetime.now() -
                                    timedelta(days=1))


class Comment(Model):
    class Meta:
        ordering = ('-created_at',)

    product = ForeignKey(Product, related_name="comments")
    text = TextField()
    created_at = DateTimeField(default=datetime.now)

    def __unicode__(self):
        return 'for product %s: %s' % (self.product, self.text)


class Like(Model):
    class Meta:
        unique_together = ('product', 'user',)

    product = ForeignKey(Product)
    user = ForeignKey(User)

    def __unicode__(self):
        return '%s likes %s' % (self.user, self.product)


@receiver(post_save, sender=Like)
def count_likes(instance, created, **kwargs):
    if created:
        instance.product.count_likes()


@receiver(pre_delete, sender=Like)
def delete_likes(instance, **kwargs):
    instance.product.decrease_likes()
