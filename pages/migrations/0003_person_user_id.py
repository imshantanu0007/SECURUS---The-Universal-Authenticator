# Generated by Django 2.1.2 on 2019-01-23 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20190121_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='user_id',
            field=models.CharField(default='999999', max_length=20),
        ),
    ]