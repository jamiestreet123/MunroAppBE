# Generated by Django 4.2.7 on 2023-12-21 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munroapp', '0010_activity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='taggedUsers',
            new_name='tagged_users',
        ),
    ]
