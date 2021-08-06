# Generated by Django 3.2.4 on 2021-08-06 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0009_alter_notification_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type_of',
            field=models.CharField(choices=[('Отклонено модератором!', 'Отклонено модератором!'), ('Лайк на статью', 'Лайк на статью'), ('Дизлайк на статью', 'Дизлайк на статью'), ('Новый комментарий', 'Новый комментарий'), ('Снято с публикации', 'Снято с публикации'), ('Комментарий удален', 'Комментарий удален'), ('Статья опубликована', 'Статья опубликована'), ('Cтатья восстановлена', 'Статья восстановлена'), ('Лайк на коммент', 'Лайк на коммент'), ('Дизлайк на коммент', 'Дизлайк на коммент'), ('Ответ на коммент', 'Ответ на коммент'), ('Аккаунт заблокирован!', 'Аккаунт заблокирован!'), ('Аккаунт разблокирован!', 'Аккаунт разблокирован!'), ('Новая жалоба', 'Новая жалоба'), ('Жалоба принята', 'Жалоба принята'), ('Жалоба отклонена', 'Жалоба отклонена')], db_index=True, max_length=50, verbose_name='тип'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]