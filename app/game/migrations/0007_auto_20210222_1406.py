# Generated by Django 3.1.5 on 2021-02-22 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20210110_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='col',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='game',
            name='row',
            field=models.IntegerField(default=-1),
        ),
    ]
