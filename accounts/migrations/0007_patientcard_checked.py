# Generated by Django 4.2.4 on 2023-08-31 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_patientcard_assistant'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientcard',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]