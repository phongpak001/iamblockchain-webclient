# Generated by Django 3.2.7 on 2022-03-21 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_testmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='view_only',
            field=models.BooleanField(default=False),
        ),
    ]
