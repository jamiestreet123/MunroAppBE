# Generated by Django 4.2.7 on 2023-12-26 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('munroapp', '0013_alter_activity_munros_alter_activity_tagged_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weather',
            name='weather',
        ),
        migrations.AddField(
            model_name='weather',
            name='description',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='weather',
            name='time',
            field=models.CharField(max_length=50),
        ),
    ]
