# Generated by Django 5.1.1 on 2024-09-10 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0005_alter_smbexercise_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='smbexercise',
            name='exDate',
            field=models.DateTimeField(default='1999-12-31 00:00:00'),
        ),
    ]
