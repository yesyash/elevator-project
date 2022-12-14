# Generated by Django 4.0.6 on 2022-07-31 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Elevator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_floor', models.IntegerField(default=1)),
                ('next_destination', models.IntegerField()),
                ('direction', models.TextField(max_length=100)),
                ('is_moving', models.BooleanField(default=False)),
                ('is_door_open', models.BooleanField(default=False)),
                ('is_working', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ElevatorSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_elevators', models.IntegerField()),
                ('number_of_floors', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_floor', models.IntegerField()),
                ('to_floor', models.IntegerField()),
                ('elevator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.elevator')),
            ],
        ),
    ]
