# Generated by Django 3.2.4 on 2021-06-29 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20210629_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='article',
            field=models.TextField(blank=True, max_length=512, verbose_name='обо мне'),
        ),
    ]
