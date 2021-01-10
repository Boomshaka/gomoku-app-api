# Generated by Django 2.0 on 2021-01-10 09:02

import django.contrib.postgres.fields
from django.db import migrations, models
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_remove_game_checker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='grid',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, default=0), size=None), blank=True, default=game.models.generate_empty_grid, size=None),
        ),
    ]
