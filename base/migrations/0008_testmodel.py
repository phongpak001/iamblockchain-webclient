# Generated by Django 3.2.7 on 2022-03-20 17:34

from django.db import migrations, models
import rules.contrib.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_sharing_view_only'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
    ]