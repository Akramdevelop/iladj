# Generated by Django 3.2.12 on 2023-09-17 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_auto_20230917_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nessacard',
            name='childsex',
            field=models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female'), ('twin', 'twin')], default='male', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='nessacard',
            name='prevbirth',
            field=models.CharField(blank=True, choices=[('normal', 'normal'), ('caesarean', 'caesarean')], default='normal', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='nessacard',
            name='typeofbirth',
            field=models.CharField(blank=True, choices=[('normal', 'normal'), ('caesarean', 'caesarean')], default='normal', max_length=255, null=True),
        ),
    ]
