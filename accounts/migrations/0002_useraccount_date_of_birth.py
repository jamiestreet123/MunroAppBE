# Generated by Django 4.2.7 on 2023-12-15 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='date_of_birth',
            field=models.DateField(default=None, null=True),
        ),
    ]