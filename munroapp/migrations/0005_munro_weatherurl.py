# Generated by Django 4.2.7 on 2023-11-28 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('munroapp', '0004_munro'),
    ]

    operations = [
        migrations.AddField(
            model_name='munro',
            name='weatherUrl',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
