# Generated by Django 3.0.6 on 2020-05-22 20:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MappedSource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('account', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SyncBag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('source', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SyncData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(-1, 'Discarded'), (0, 'Current'), (1, 'Readonly')])),
                ('created', models.DateTimeField()),
                ('dataString0', models.URLField()),
                ('dataString1', models.DateTimeField()),
                ('dataString2', models.TextField(blank=True)),
                ('dataString3', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('/[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[A-Za-z][ ]*[A-Za-z]/')])),
                ('dataString4', models.CharField(blank=True, max_length=40)),
                ('dataString5', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SyncItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('grade', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=1)),
                ('currentData', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='application.SyncData', verbose_name='current data')),
                ('syncBag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.SyncBag')),
            ],
        ),
    ]
