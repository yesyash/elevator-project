# Generated by Django 4.0.6 on 2022-07-31 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_elevator_next_destination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevator',
            name='direction',
            field=models.TextField(max_length=100, null=True),
        ),
    ]