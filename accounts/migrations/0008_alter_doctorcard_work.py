# Generated by Django 4.2.4 on 2023-09-01 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_patientcard_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorcard',
            name='work',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]