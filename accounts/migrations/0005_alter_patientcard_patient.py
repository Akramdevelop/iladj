# Generated by Django 4.2.4 on 2023-08-31 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_doctorcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientcard',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patientprofile'),
        ),
    ]
