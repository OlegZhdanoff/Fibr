# Generated by Django 3.2.4 on 2021-07-26 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0010_merge_20210714_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blocked_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]