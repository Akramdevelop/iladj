# Generated by Django 4.2.4 on 2023-08-31 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_patientcard_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientcard',
            name='assistant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.assistantprofile'),
        ),
    ]
