# Generated by Django 4.2.7 on 2023-12-21 13:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('munroapp', '0012_alter_activity_dateadded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='munros',
            field=models.ManyToManyField(blank=True, to='munroapp.munro'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='tagged_users',
            field=models.ManyToManyField(blank=True, related_name='taggedUserToUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
