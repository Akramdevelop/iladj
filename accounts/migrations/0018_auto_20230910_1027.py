# Generated by Django 3.2.12 on 2023-09-10 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_doctordiagnosis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorcard',
            name='isMaried',
        ),
        migrations.RemoveField(
            model_name='doctorcard',
            name='isSmoker',
        ),
        migrations.RemoveField(
            model_name='doctorcard',
            name='type',
        ),
        migrations.RemoveField(
            model_name='doctorcard',
            name='work',
        ),
        migrations.AddField(
            model_name='patientcard',
            name='isMaried',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patientcard',
            name='isSmoker',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patientcard',
            name='type',
            field=models.CharField(choices=[('check', 'check'), ('recheck', 'recheck'), ('operation', 'operation')], default='check', max_length=255),
        ),
        migrations.AddField(
            model_name='patientcard',
            name='work',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='DoctorDiagnosis',
        ),
    ]
