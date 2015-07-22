# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_userprofile_liked_boards'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='liked_boards',
            new_name='upvoted_boards',
        ),
    ]
