# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('created_at',
                 models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(max_digits=19,
                                              decimal_places=2)),
                ('created_at',
                 models.DateTimeField(default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('likes', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='product',
            field=models.ForeignKey(to='product.Product'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(related_name='comments',
                                    to='product.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set([('product', 'user')]),
        ),
    ]
