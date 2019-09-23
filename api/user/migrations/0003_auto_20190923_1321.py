# Generated by Django 2.2.5 on 2019-09-23 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190923_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banlist',
            name='ip',
        ),
        migrations.AddField(
            model_name='banlist',
            name='ip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.IPlist'),
        ),
        migrations.RemoveField(
            model_name='banlist',
            name='user',
        ),
        migrations.AddField(
            model_name='banlist',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Profile'),
        ),
    ]
