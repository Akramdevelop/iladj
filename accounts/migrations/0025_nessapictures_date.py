# Generated by Django 3.2.12 on 2023-09-14 22:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_nessapictures'),
    ]

    operations = [
        migrations.AddField(
            model_name='nessapictures',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]