# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_billboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='liked_boards',
            field=models.ManyToManyField(to='website.Billboard', blank=True),
        ),
    ]
