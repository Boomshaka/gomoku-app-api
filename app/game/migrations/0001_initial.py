# Generated by Django 3.1.4 on 2021-01-02 09:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('winner', models.IntegerField(choices=[(1, 'one'), (2, 'two'), (0, 'zero')], default=0)),
                ('status', models.CharField(choices=[('Started', 'started'), ('Playing', 'playing'), ('Finished', 'finished')], default='Started', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
