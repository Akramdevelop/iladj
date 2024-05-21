# Generated by Django 3.2.12 on 2023-09-10 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20230910_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='checkprice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='operationprice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='recheckprice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
