# Generated by Django 3.2.4 on 2021-06-22 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('short_description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Тематика',
                'verbose_name_plural': 'Тематики',
            },
        ),
    ]
