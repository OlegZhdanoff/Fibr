# Generated by Django 3.2.4 on 2021-06-30 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_alter_userprofile_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='static/img/default.jpg', upload_to='users_avatars'),
        ),
    ]
