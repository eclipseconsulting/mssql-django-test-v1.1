# Generated by Django 3.1.14 on 2021-12-27 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0002_auto_20211227_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widget',
            name='url',
            field=models.TextField(blank=True),
        ),
    ]
