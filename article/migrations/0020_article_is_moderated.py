# Generated by Django 3.2.4 on 2021-07-14 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0019_auto_20210714_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_moderated',
            field=models.BooleanField(db_index=True, default=False, verbose_name='На модерацию'),
        ),
    ]