# Generated by Django 4.0.6 on 2022-07-31 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_requests_completes_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='completes_by',
            field=models.IntegerField(null=True),
        ),
    ]
