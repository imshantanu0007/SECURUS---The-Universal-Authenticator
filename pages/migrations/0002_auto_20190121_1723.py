# Generated by Django 2.1.5 on 2019-01-21 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p1', models.CharField(max_length=20)),
            ],
        ),
        migrations.RenameModel(
            old_name='Users',
            new_name='person',
        ),
        migrations.AddField(
            model_name='detail',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.person'),
        ),
    ]